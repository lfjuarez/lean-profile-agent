#!/usr/bin/env bash
# Deploy lean-profile-agent to Google Cloud Run. Nothing here runs on its own: read, then run.
#
# Prerequisites (one time):
#   gcloud auth login
#   gcloud config set project "$PROJECT"
#   gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
#       secretmanager.googleapis.com artifactregistry.googleapis.com
#
# The model key goes to Secret Manager, never into the image or the repo. Default provider is
# Gemini Flash-Lite on its free tier (PROVIDER=gemini); set PROVIDER=anthropic to use Claude.
#   printf '%s' "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-
#   (or: printf '%s' "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key --data-file=-)
#   (later rotations: gcloud secrets versions add <secret> --data-file=-)
#   gcloud secrets add-iam-policy-binding gemini-api-key \
#       --member="serviceAccount:$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')-compute@developer.gserviceaccount.com" \
#       --role=roles/secretmanager.secretAccessor
set -euo pipefail

PROJECT="${PROJECT:?set PROJECT to the GCP project id}"
REGION="${REGION:-southamerica-east1}"
SERVICE="${SERVICE:-lean-profile-agent}"
PROVIDER="${PROVIDER:-gemini}"

case "$PROVIDER" in
  gemini) SECRETS="GEMINI_API_KEY=gemini-api-key:latest"; EXTRA_ENV="GEMINI_MODEL=${GEMINI_MODEL:-gemini-flash-lite-latest}" ;;
  anthropic) SECRETS="ANTHROPIC_API_KEY=anthropic-api-key:latest"; EXTRA_ENV="PROFILE_MODEL=${PROFILE_MODEL:-claude-sonnet-5-5}" ;;
  *) echo "PROVIDER must be gemini or anthropic"; exit 1 ;;
esac

cd "$(dirname "$0")/.."
test -f cv/Leandro_Juarez_CV_EN.pdf -a -f cv/Leandro_Juarez_CV_ES.pdf \
  || { echo "put the CV PDFs in cv/ first (see cv/README.md)"; exit 1; }

gcloud run deploy "$SERVICE" \
  --project "$PROJECT" \
  --region "$REGION" \
  --source . \
  --allow-unauthenticated \
  --port 8080 \
  --cpu 1 --memory 512Mi \
  --min-instances 0 --max-instances 2 \
  --concurrency 20 \
  --timeout 120 \
  --set-secrets "$SECRETS" \
  --set-env-vars "PROFILE_PROVIDER=$PROVIDER,$EXTRA_ENV,CHAT_DAILY_LIMIT=${CHAT_DAILY_LIMIT:-300},LOG_LEVEL=INFO"

URL="$(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format='value(status.url)')"
echo "Deployed: $URL"
echo "MCP endpoint: $URL/mcp"
curl -fsS "$URL/health" && echo
