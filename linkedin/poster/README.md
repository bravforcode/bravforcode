# LinkedIn poster (direct Posts API)

Publishes the approved LinkedIn drafts on schedule from a VPS, without depending on any chat session.

Slots (Thailand time): JIL paper 10:00, morning 13:00, evening 20:00.

## Files
- `build_schedule.py` reads the drafts in `linkedin/posts/` and writes `schedule.json`. Edit the drafts, rebuild, redeploy.
- `poster.py` publishes due items. Stdlib only. `--dry-run` prints what would post without any network call.
- `test_poster.py` unit tests: `python3 -m unittest -v test_poster`
- `systemd/` service and 5-minute timer.
- `env.example` variables the service needs.

## Safety rules built in
- An item publishes only within 6 hours after its slot. Older items are marked `missed`, never posted late.
- State is written before each call (`sending`). A leftover `sending` entry is reported and never retried automatically, because the post may already be live.
- Items with a `urn` (already published) are skipped.
- Drafts stay plain text. `poster.py` escapes the characters LinkedIn's `little` text format reserves (`| { } @ [ ] ( ) < > # \ * _ ~`), so parentheses and underscores post as written. A `#` therefore posts as plain text, not a hashtag link.
- One automatic retry, only when the post was certainly not created: HTTP 429, or a connection that never got a response. A 5xx or a read timeout may arrive after LinkedIn created the post, so those are recorded as `failed` instead of risking a duplicate.
- A failed item records LinkedIn's response body in `state.json` and the journal.

## One-time setup on the VPS
1. Create the user and directories:
   `sudo useradd --system --home /opt/linkedin-poster --shell /usr/sbin/nologin linkedin-poster`
   `sudo mkdir -p /opt/linkedin-poster /var/lib/linkedin-poster /etc/linkedin-poster`
   `sudo chown linkedin-poster:linkedin-poster /var/lib/linkedin-poster`
2. Leave the server timezone alone on a shared VPS. Every slot carries `+07:00` and the timer runs every 5 minutes, so the poster does not depend on it, while other timers and cron jobs on the machine fire in local time. Read logs in Thai time with `TZ=Asia/Bangkok journalctl -u linkedin-poster`.
3. Copy `poster.py` and `schedule.json` to `/opt/linkedin-poster/`.
4. Create `/etc/linkedin-poster/env` from `env.example`, fill `LINKEDIN_ACCESS_TOKEN`, then `sudo chmod 600` it.
5. Install units: copy `systemd/*` to `/etc/systemd/system/`, then `sudo systemctl daemon-reload`.
6. Dry run first: `sudo -u linkedin-poster python3 /opt/linkedin-poster/poster.py --dry-run --schedule /opt/linkedin-poster/schedule.json`
7. Enable: `sudo systemctl enable --now linkedin-poster.timer`
8. Watch: `journalctl -u linkedin-poster -f`

## Updating the schedule
Run `build_schedule.py` in the repo, copy the new `schedule.json` to `/opt/linkedin-poster/`. The next timer run picks it up.

## Checking the token without posting
LinkedIn's token introspection returns whether the token is active, its scopes and its expiry, and creates nothing. It needs the app's client ID and secret. Put them in a root-only file so they never appear in shell history or process arguments:
```
sudo install -m 600 /dev/null /root/li-introspect
sudoedit /root/li-introspect   # one line: client_id=...&client_secret=...&token=...
sudo curl -s -X POST https://www.linkedin.com/oauth/v2/introspectToken   -H 'Content-Type: application/x-www-form-urlencoded' --data @/root/li-introspect
sudo shred -u /root/li-introspect
```
Expect `"active":true`, a `scope` containing `w_member_social`, and `expires_at` (Unix seconds). Put the expiry date in a calendar with a reminder a week before.

## Failures and token renewal
- A failed item is recorded as `failed` and is not retried automatically. The journal shows it. To retry while its window is still open, delete its entry from `/var/lib/linkedin-poster/state.json` and run the service once.
- When the access token expires, every item in its window fails. Renew the token, update `/etc/linkedin-poster/env`, then retry the failed items as above.
