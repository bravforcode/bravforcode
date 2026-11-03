#!/usr/bin/env python3
"""Renew the LinkedIn access token with the stored refresh token before it expires.

Standard library only. Run daily from linkedin-token-refresh.timer as root, because it rewrites files in
/etc/linkedin-poster.
- Does nothing while the access token has more than RENEW_BEFORE left.
- Rewrites only the LINKEDIN_ACCESS_TOKEN line of the env file, atomically, so the poster never reads a half-written file.
- Exit code 1 when renewal fails, or when the refresh token itself is close to its end. LinkedIn does not extend a
  refresh token, so that case needs a new sign-in, and the unit failing is what raises the alert.
- Never prints a token.

Environment: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET (only needed when a renewal is due).
"""
import argparse, datetime as dt, json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
RENEW_BEFORE = 14 * 86400
SIGN_IN_WARNING = 30 * 86400


def iso(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()


def replace_token_line(env_text, token):
    lines = env_text.splitlines(keepends=True)
    idx = [i for i, line in enumerate(lines) if line.startswith("LINKEDIN_ACCESS_TOKEN=")]
    if len(idx) != 1:
        raise ValueError("env file must contain exactly one LINKEDIN_ACCESS_TOKEN= line")
    lines[idx[0]] = f"LINKEDIN_ACCESS_TOKEN={token}\n"
    return "".join(lines)


def write_private(path, text):
    p = pathlib.Path(path)
    tmp = p.with_name(p.name + ".tmp")
    tmp.unlink(missing_ok=True)
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, p)


def request_new_token(refresh_token, client_id, client_secret, opener=urllib.request.urlopen):
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with opener(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv=None, now=None, opener=urllib.request.urlopen):
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="/etc/linkedin-poster/env")
    ap.add_argument("--refresh", default="/etc/linkedin-poster/refresh.json")
    args = ap.parse_args(argv)

    now = int(time.time() if now is None else now)
    refresh = json.loads(pathlib.Path(args.refresh).read_text(encoding="utf-8"))
    access_end = refresh["obtained_at"] + refresh["expires_in"]
    refresh_end = refresh["obtained_at"] + refresh["refresh_token_expires_in"]

    status = 0
    if refresh_end - now < SIGN_IN_WARNING:
        print(f"SIGN-IN NEEDED: the refresh token ends {iso(refresh_end)}; run the OAuth sign-in again before then",
              file=sys.stderr)
        status = 1

    if access_end - now > RENEW_BEFORE:
        print(f"OK access token valid until {iso(access_end)}, {(access_end - now) // 86400} days left")
        return status

    client_id = os.environ.get("LINKEDIN_CLIENT_ID")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET must be set", file=sys.stderr)
        return 2

    try:
        data = request_new_token(refresh["refresh_token"], client_id, client_secret, opener)
        token = data["access_token"]
        expires_in = int(data["expires_in"])
    except Exception as exc:
        detail = f"{type(exc).__name__}: {exc}"
        if isinstance(exc, urllib.error.HTTPError):
            detail += " " + exc.read().decode("utf-8", "replace")
        print(f"FAILED renewal: {detail[:500]}", file=sys.stderr)
        return 1

    env_path = pathlib.Path(args.env)
    write_private(env_path, replace_token_line(env_path.read_text(encoding="utf-8"), token))
    # The env file is written first: if this second write fails, the next run renews again instead of trusting
    # a refresh.json that claims a token the env file does not have.
    write_private(args.refresh, json.dumps({
        "refresh_token": data.get("refresh_token", refresh["refresh_token"]),
        "refresh_token_expires_in": int(data.get("refresh_token_expires_in", refresh_end - now)),
        "obtained_at": now,
        "expires_in": expires_in,
    }))
    print(f"RENEWED access token, valid until {iso(now + expires_in)}")
    return status


if __name__ == "__main__":
    sys.exit(main())
