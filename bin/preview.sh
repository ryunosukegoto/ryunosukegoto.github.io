#!/usr/bin/env bash
#
# Preview the site locally.
#
#     bin/preview.sh
#
# Builds the site, serves it at http://127.0.0.1:4000, then watches your files and
# rebuilds whenever you save. Just refresh the browser to see changes.
# Press Ctrl-C to stop.
#
#     PORT=8080 bin/preview.sh     # use a different port
#
set -uo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-4000}"
DEST="_site"
WATCH=(_data _includes _layouts assets/css *.html _posts _config.yml)

# --- pick a Jekyll -------------------------------------------------------------------
# Preferred: a modern Ruby with the Gemfile installed (`brew install ruby && bundle install`).
# Fallback: the pinned gem set in ~/.gem-jekyll, which works with the Ruby macOS ships.
if command -v bundle >/dev/null 2>&1 && bundle exec jekyll -v >/dev/null 2>&1; then
  build() { bundle exec jekyll build --quiet --destination "$DEST"; }
  ENGINE="bundle exec jekyll"
elif [ -d "$HOME/.gem-jekyll" ]; then
  build() {
    GEM_HOME="$HOME/.gem-jekyll" SITE="$DEST" LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
      ruby -rrubygems -e 'Gem.paths = ENV; load "bin/_jekyll_build.rb"'
  }
  ENGINE="ruby + ~/.gem-jekyll"
else
  cat <<'MSG' >&2
No Jekyll available.

Either install a modern Ruby and the project gems:
    brew install ruby        # then reopen your terminal
    bundle install

...or ask Claude to re-create the pinned gem set in ~/.gem-jekyll.
MSG
  exit 1
fi

# --- signature of the watched tree ---------------------------------------------------
signature() {
  find "${WATCH[@]}" -type f ! -path "./$DEST/*" -print0 2>/dev/null \
    | xargs -0 stat -f '%m %z %N' 2>/dev/null | sort | cksum
}

cleanup() {
  [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null
  printf '\nstopped\n'
  exit 0
}
trap cleanup INT TERM

# --- first build ---------------------------------------------------------------------
printf 'building with %s ...\n' "$ENGINE"
build || exit 1

python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$DEST" >/dev/null 2>&1 &
SERVER_PID=$!
sleep 1

cat <<MSG

  ready:  http://127.0.0.1:$PORT/
          http://127.0.0.1:$PORT/japanese.html

  watching for changes — edit a file, then refresh your browser.
  Ctrl-C to stop.

MSG

# --- watch loop ----------------------------------------------------------------------
LAST="$(signature)"
while true; do
  sleep 1.5
  NOW="$(signature)"
  if [ "$NOW" != "$LAST" ]; then
    LAST="$NOW"
    printf '%s  change detected — rebuilding ... ' "$(date '+%H:%M:%S')"
    if build; then :; else printf 'build failed (site left as it was)\n'; fi
  fi
done
