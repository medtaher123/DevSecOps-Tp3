# - slim base (fewer packages, smaller CVE surface)
# - no secrets in ENV or layers
# - non-root user
# - no pip cache
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOST=0.0.0.0 \
    DB_PATH=/tmp/users.db

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R appuser:appuser /app

COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 5000
CMD ["python", "app.py"]


