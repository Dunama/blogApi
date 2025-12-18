
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (Pillow + optional Postgres driver)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		libjpeg62-turbo-dev \
		zlib1g-dev \
		libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy Django project
COPY blog_api/ /app/

EXPOSE 8000

# docker-compose overrides this for local dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

