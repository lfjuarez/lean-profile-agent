# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PORT=8080
WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .

# Knowledge base and CV PDFs are read at runtime, not packaged.
COPY knowledge ./knowledge
COPY cv ./cv
ENV PROFILE_KB_DIR=/app/knowledge PROFILE_CV_DIR=/app/cv

RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app
EXPOSE 8080
CMD ["profile-agent"]
