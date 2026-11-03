import io, json, os, pathlib, tempfile, unittest, urllib.error, urllib.parse
import refresh_token

DAY = 86400
NOW = 1_800_000_000
ENV = "# comment\nLINKEDIN_ACCESS_TOKEN=old\nLINKEDIN_AUTHOR_URN=urn:li:person:x\n"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
    def read(self):
        return json.dumps(self.payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        return False


class Refresh(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.env = pathlib.Path(self.dir.name, "env")
        self.refresh = pathlib.Path(self.dir.name, "refresh.json")
        self.env.write_text(ENV, encoding="utf-8")
        os.environ["LINKEDIN_CLIENT_ID"] = "cid"
        os.environ["LINKEDIN_CLIENT_SECRET"] = "secret"

    def tearDown(self):
        self.dir.cleanup()
        os.environ.pop("LINKEDIN_CLIENT_ID", None)
        os.environ.pop("LINKEDIN_CLIENT_SECRET", None)

    def write_refresh(self, access_days_left, refresh_days_left):
        self.refresh.write_text(json.dumps({
            "refresh_token": "rt", "obtained_at": NOW - DAY,
            "expires_in": (access_days_left + 1) * DAY,
            "refresh_token_expires_in": (refresh_days_left + 1) * DAY,
        }), encoding="utf-8")

    def run_main(self, opener):
        return refresh_token.main(["--env", str(self.env), "--refresh", str(self.refresh)], now=NOW, opener=opener)

    def test_not_due_makes_no_call_and_changes_nothing(self):
        self.write_refresh(access_days_left=30, refresh_days_left=300)
        before = self.refresh.read_text(encoding="utf-8")
        def opener(req, timeout):
            raise AssertionError("no network call expected")
        self.assertEqual(self.run_main(opener), 0)
        self.assertEqual(self.env.read_text(encoding="utf-8"), ENV)
        self.assertEqual(self.refresh.read_text(encoding="utf-8"), before)

    def test_due_renews_token_line_only_and_updates_expiry(self):
        self.write_refresh(access_days_left=10, refresh_days_left=300)
        seen = {}
        def opener(req, timeout):
            seen["form"] = urllib.parse.parse_qs(req.data.decode("utf-8"))
            return FakeResponse({"access_token": "new", "expires_in": 60 * DAY,
                                 "refresh_token": "rt2", "refresh_token_expires_in": 290 * DAY})
        self.assertEqual(self.run_main(opener), 0)
        self.assertEqual(seen["form"]["grant_type"], ["refresh_token"])
        self.assertEqual(seen["form"]["refresh_token"], ["rt"])
        self.assertEqual(self.env.read_text(encoding="utf-8"), ENV.replace("=old", "=new"))
        stored = json.loads(self.refresh.read_text(encoding="utf-8"))
        self.assertEqual(stored, {"refresh_token": "rt2", "refresh_token_expires_in": 290 * DAY,
                                  "obtained_at": NOW, "expires_in": 60 * DAY})
        if os.name == "posix":
            self.assertEqual(self.env.stat().st_mode & 0o777, 0o600)

    def test_failed_renewal_exits_1_and_keeps_old_token(self):
        self.write_refresh(access_days_left=10, refresh_days_left=300)
        def opener(req, timeout):
            raise urllib.error.HTTPError("u", 400, "Bad Request", {}, io.BytesIO(b'{"error":"invalid_request"}'))
        self.assertEqual(self.run_main(opener), 1)
        self.assertEqual(self.env.read_text(encoding="utf-8"), ENV)

    def test_refresh_token_near_end_exits_1_to_raise_alert(self):
        self.write_refresh(access_days_left=30, refresh_days_left=20)
        self.assertEqual(self.run_main(lambda req, timeout: None), 1)


if __name__ == "__main__":
    unittest.main()
