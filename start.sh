#!/usr/bin/env sh
set -eu

# Run DB migrations on startup (safe to re-run)
python blog_api/manage.py migrate --noinput

# Start Gunicorn and bind to Render's injected PORT
: "${PORT:=8000}"
: "${WEB_CONCURRENCY:=1}"

gunicorn blog.wsgi:application \
  --chdir blog_api \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WEB_CONCURRENCY}" \
  --log-level info
