#!/usr/bin/env bash
# Every page of the site answers 200 over HTTPS (PLAN.md W1 step 5), and an unknown page 404.
# usage: bash tools/check.sh [base_url]
set -u
BASE="${1:-https://sriramgoparaju.github.io/lumiwire-site}"
fail=0
for p in "" how-to-play/ support/ privacy/ terms/ delete-account/ robots.txt sitemap.xml 404.html \
  assets/site.css assets/icon-192.png assets/screen-home.webp assets/obstacle-via.webp; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -I "$BASE/$p")
  printf '%s  %s/%s\n' "$code" "$BASE" "$p"
  [ "$code" = "200" ] || fail=1
done
code=$(curl -s -o /dev/null -w '%{http_code}' -I "$BASE/no-such-page/")
printf '%s  %s/no-such-page/ (expect 404)\n' "$code" "$BASE"
[ "$code" = "404" ] || fail=1
[ $fail = 0 ] && echo PASS || { echo FAIL; exit 1; }
