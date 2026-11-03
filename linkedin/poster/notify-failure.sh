#!/usr/bin/env bash
# Run by linkedin-poster-notify@.service when linkedin-poster or linkedin-token-refresh fails (see OnFailure= in those units).
# Always writes a journal line. Sends Telegram only when both variables are set in /etc/linkedin-poster/alert.env.
set -euo pipefail

unit="${1:?usage: notify-failure.sh <unit-name>}"
msg="linkedin-poster: $unit failed on $(hostname) at $(date -Is). Check: journalctl -u $unit -n 50"
logger -t linkedin-poster-alert -p user.crit -- "$msg"

# At most one Telegram message per unit per hour, so a failure that repeats every 5 minutes does not flood the chat.
stamp="/var/lib/linkedin-poster/.alert-$unit"
if [ -f "$stamp" ] && [ -z "$(find "$stamp" -mmin +60)" ]; then
    exit 0
fi
touch "$stamp"

if [ -n "${LINKEDIN_ALERT_TELEGRAM_TOKEN:-}" ] && [ -n "${LINKEDIN_ALERT_TELEGRAM_CHAT_ID:-}" ]; then
    # The URL carries the bot token, so it goes through curl's stdin config and never appears in argv.
    printf 'url = "https://api.telegram.org/bot%s/sendMessage"\n' "$LINKEDIN_ALERT_TELEGRAM_TOKEN" \
        | curl -sS --fail --max-time 15 -K - \
            --data-urlencode "chat_id=$LINKEDIN_ALERT_TELEGRAM_CHAT_ID" \
            --data-urlencode "text=$msg" -o /dev/null
fi
