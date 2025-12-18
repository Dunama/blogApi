#!/usr/bin/env sh
set -e

# Run migrations every boot (safe and idempotent)
python blog_api/manage.py migrate --noinput

# Optional: collectstatic if you ever remove it from build
# python blog_api/manage.py collectstatic --noinput

# Start the WSGI server
exec gunicorn blog.wsgi:application --chdir blog_api --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile - --log-level info
