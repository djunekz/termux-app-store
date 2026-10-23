FROM python:3.15-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE MANIFEST.in ./
COPY termux_app_store ./termux_app_store

RUN pip install --no-cache-dir .

ENTRYPOINT ["termux-app-store"]
