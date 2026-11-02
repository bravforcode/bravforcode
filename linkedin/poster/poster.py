#!/usr/bin/env python3
"""Publish due LinkedIn items through the Posts API (POST https://api.linkedin.com/rest/posts).

Standard library only, so the VPS needs no installs. Run every few minutes from a systemd timer.
- Items publish only inside a catch-up window after their slot; older items are marked missed, never posted late.
- State is written before each call ('sending') and after success (urn). A leftover 'sending' entry is
  reported and never retried automatically, because the post may already be live.
- Commentary is escaped for LinkedIn's "little" text format, so drafts stay plain text.
- Exit code 1 if any item failed, so the unit shows as failed and an alert can fire.

Environment: LINKEDIN_ACCESS_TOKEN (required unless --dry-run), LINKEDIN_AUTHOR_URN (required unless --dry-run),
LINKEDIN_VERSION (YYYYMM, default 202610; check the current version in the LinkedIn docs).
"""
import argparse, datetime as dt, json, os, pathlib, sys, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
API = "https://api.linkedin.com/rest/posts"
CATCH_UP = dt.timedelta(hours=6)
RETRY_DELAY_SECONDS = 10
# Reserved by LinkedIn's "little" text format; each must be backslash-escaped or the post is cut or rejected.
LITTLE_RESERVED = set("|{}@[]()<>#\\*_~")


def escape_little(text):
    return "".join("\\" + c if c in LITTLE_RESERVED else c for c in text)


def load(path, default):
    p = pathlib.Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def save(path, data):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def due_items(schedule, state, now):
    """Return (to_post, missed). Skips items already published, already attempted, or marked missed."""
    to_post, missed = [], []
    for item in schedule:
        if "urn" in item or item.get("missed") or item["id"] in state:
            continue
        at = dt.datetime.fromisoformat(item["at"])
        if at > now:
            continue
        (to_post if now - at <= CATCH_UP else missed).append(item)
    return to_post, missed


def create_post(text, token, author, version, opener=urllib.request.urlopen):
    body = json.dumps({
        "author": author,
        "commentary": escape_little(text),
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": version,
    })
    with opener(req, timeout=30) as resp:
        if resp.status != 201:
            raise RuntimeError(f"unexpected status {resp.status}")
        urn = resp.headers.get("x-restli-id")
        if not urn:
            raise RuntimeError("201 response without x-restli-id")
        return urn


def create_post_with_retry(text, token, author, version, opener=urllib.request.urlopen, sleep=time.sleep):
    """Retry once only when the post was certainly not created: 429, or a connection that never got a response.
    A 5xx or a read timeout may come after LinkedIn created the post, so those fail instead of risking a duplicate."""
    try:
        return create_post(text, token, author, version, opener)
    except urllib.error.HTTPError as err:
        if err.code != 429:
            raise
    except urllib.error.URLError:
        pass
    sleep(RETRY_DELAY_SECONDS)
    return create_post(text, token, author, version, opener)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", default=str(HERE / "schedule.json"))
    ap.add_argument("--state", default=str(HERE / "state.json"))
    ap.add_argument("--now", help="ISO time with offset, for tests and dry runs")
    ap.add_argument("--dry-run", action="store_true", help="print what would be posted; no network, no state change")
    args = ap.parse_args(argv)

    now = dt.datetime.fromisoformat(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    schedule = load(args.schedule, [])
    state = load(args.state, {})
    to_post, missed = due_items(schedule, state, now)

    for item in schedule:
        if state.get(item["id"], {}).get("status") == "sending":
            print(f"CHECK {item['id']}: previous run stopped mid-send; verify on LinkedIn before doing anything", file=sys.stderr)

    if args.dry_run:
        for item in missed:
            print(f"WOULD SKIP (missed) {item['id']}")
        for item in to_post:
            print(f"WOULD POST {item['id']} at {item['at']}")
        return 0

    for item in missed:
        state[item["id"]] = {"status": "missed", "at": item["at"]}
        print(f"MISSED {item['id']}: outside the {CATCH_UP} catch-up window, not posted")
    save(args.state, state)

    if not to_post:
        return 0

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author = os.environ.get("LINKEDIN_AUTHOR_URN")
    version = os.environ.get("LINKEDIN_VERSION", "202610")
    if not token or not author:
        print("LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_URN must be set", file=sys.stderr)
        return 2

    failed = False
    for item in to_post:
        state[item["id"]] = {"status": "sending", "at": now.isoformat()}
        save(args.state, state)
        try:
            urn = create_post_with_retry(item["text"], token, author, version)
        except Exception as exc:  # record and continue with the next item
            detail = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                detail += " " + exc.read().decode("utf-8", "replace")
            state[item["id"]] = {"status": "failed", "error": detail[:500], "at": now.isoformat()}
            save(args.state, state)
            print(f"FAILED {item['id']}: {detail[:500]}", file=sys.stderr)
            failed = True
            continue
        state[item["id"]] = {"status": "posted", "urn": urn, "at": now.isoformat()}
        save(args.state, state)
        print(f"POSTED {item['id']} {urn}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
