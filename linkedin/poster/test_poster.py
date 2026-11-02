import datetime as dt, io, json, tempfile, unittest, urllib.error, pathlib
import poster

BKK = dt.timezone(dt.timedelta(hours=7))


def item(id_, at, **extra):
    return {"id": id_, "at": at, "text": f"text {id_}", **extra}


class FakeResponse:
    def __init__(self, status, headers):
        self.status = status
        self.headers = headers
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        return False


class DueItems(unittest.TestCase):
    def test_future_items_wait(self):
        now = dt.datetime(2026, 11, 3, 9, 0, tzinfo=BKK)
        to_post, missed = poster.due_items([item("a", "2026-11-03T10:00:00+07:00")], {}, now)
        self.assertEqual((to_post, missed), ([], []))

    def test_due_inside_window_is_posted(self):
        now = dt.datetime(2026, 11, 3, 10, 30, tzinfo=BKK)
        to_post, missed = poster.due_items([item("a", "2026-11-03T10:00:00+07:00")], {}, now)
        self.assertEqual([i["id"] for i in to_post], ["a"])
        self.assertEqual(missed, [])

    def test_due_outside_window_is_missed_not_posted(self):
        now = dt.datetime(2026, 11, 3, 18, 0, tzinfo=BKK)
        to_post, missed = poster.due_items([item("a", "2026-11-03T10:00:00+07:00")], {}, now)
        self.assertEqual(to_post, [])
        self.assertEqual([i["id"] for i in missed], ["a"])

    def test_published_or_attempted_items_are_skipped(self):
        now = dt.datetime(2026, 11, 3, 10, 30, tzinfo=BKK)
        schedule = [item("a", "2026-11-03T10:00:00+07:00", urn="urn:li:share:1"),
                    item("b", "2026-11-03T10:00:00+07:00", missed=True),
                    item("c", "2026-11-03T10:00:00+07:00")]
        to_post, _ = poster.due_items(schedule, {"c": {"status": "sending"}}, now)
        self.assertEqual(to_post, [])


class CreatePost(unittest.TestCase):
    def test_sends_required_headers_and_body_and_returns_urn(self):
        seen = {}
        def opener(req, timeout):
            seen["headers"] = {k.lower(): v for k, v in req.header_items()}
            seen["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse(201, {"x-restli-id": "urn:li:share:99"})
        urn = poster.create_post("hello", "tok", "urn:li:person:x", "202610", opener)
        self.assertEqual(urn, "urn:li:share:99")
        self.assertEqual(seen["headers"]["authorization"], "Bearer tok")
        self.assertEqual(seen["headers"]["linkedin-version"], "202610")
        self.assertEqual(seen["headers"]["x-restli-protocol-version"], "2.0.0")
        self.assertEqual(seen["body"]["commentary"], "hello")
        self.assertEqual(seen["body"]["lifecycleState"], "PUBLISHED")
        self.assertEqual(seen["body"]["visibility"], "PUBLIC")

    def test_retries_once_on_server_error(self):
        calls = []
        def opener(req, timeout):
            calls.append(1)
            if len(calls) == 1:
                raise urllib.error.HTTPError(req.full_url, 502, "bad gateway", {}, io.BytesIO(b""))
            return FakeResponse(201, {"x-restli-id": "urn:li:share:7"})
        urn = poster.create_post_with_retry("hi", "t", "a", "202610", opener, sleep=lambda s: None)
        self.assertEqual((urn, len(calls)), ("urn:li:share:7", 2))

    def test_does_not_retry_client_error(self):
        calls = []
        def opener(req, timeout):
            calls.append(1)
            raise urllib.error.HTTPError(req.full_url, 403, "forbidden", {}, io.BytesIO(b""))
        with self.assertRaises(urllib.error.HTTPError):
            poster.create_post_with_retry("hi", "t", "a", "202610", opener, sleep=lambda s: None)
        self.assertEqual(len(calls), 1)


class MainDryRun(unittest.TestCase):
    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            sched = pathlib.Path(d, "schedule.json")
            state = pathlib.Path(d, "state.json")
            sched.write_text(json.dumps([item("a", "2026-11-03T10:00:00+07:00")]), encoding="utf-8")
            code = poster.main(["--schedule", str(sched), "--state", str(state),
                                "--now", "2026-11-03T10:30:00+07:00", "--dry-run"])
            self.assertEqual(code, 0)
            self.assertFalse(state.exists())


class RealSchedule(unittest.TestCase):
    def test_generated_schedule_has_no_duplicate_ids_and_valid_times(self):
        path = pathlib.Path(__file__).with_name("schedule.json")
        items = json.loads(path.read_text(encoding="utf-8"))
        ids = [i["id"] for i in items]
        self.assertEqual(len(ids), len(set(ids)))
        for i in items:
            dt.datetime.fromisoformat(i["at"])
            self.assertTrue(i["text"].strip())


if __name__ == "__main__":
    unittest.main()
