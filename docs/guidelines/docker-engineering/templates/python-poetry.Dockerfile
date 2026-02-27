# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apt 
    apt-get update && 
    apt-get install -y --no-install-recommends build-essential
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache/pypoetry 
    poetry install --no-root

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" 
    PYTHONUNBUFFERED=1
COPY src/ src/
# Non-root UID
USER 1000
ENTRYPOINT ["python"]
CMD ["-m", "src.main"]
