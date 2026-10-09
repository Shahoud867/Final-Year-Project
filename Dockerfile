# Granite: one image that serves the API and the built web UI.
#   docker build -t granite .
#   docker run -p 8000:8000 -v granite-data:/data granite
# Defaults to recorded mode (saved real model answers), so it runs with no model server and no cost.

FROM node:22-slim AS web
WORKDIR /web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY apps/web/ ./
RUN npm run build

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY packages/granite_core packages/granite_core
COPY workflows/refund_desk workflows/refund_desk
COPY apps/api apps/api
RUN pip install ./packages/granite_core ./workflows/refund_desk ./apps/api \
    && rm -rf packages/granite_core/tests workflows/refund_desk/tests apps/api/tests
COPY data/seed data/seed
COPY data/cassettes/refund_desk_v1.json data/cassettes/refund_desk_v1.json
COPY --from=web /web/dist /app/web

RUN useradd --system --uid 10001 --home /app granite && mkdir /data && chown granite /data
USER granite
ENV GRANITE_DB_URL=sqlite:////data/granite.db \
    GRANITE_SEED_DIR=/app/data/seed \
    GRANITE_CASSETTE=/app/data/cassettes/refund_desk_v1.json \
    GRANITE_STATIC_DIR=/app/web \
    GRANITE_LLM_MODE=recorded
VOLUME /data
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=4s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["uvicorn", "granite_api.main:app_from_env", "--factory", "--host", "0.0.0.0", "--port", "8000"]
