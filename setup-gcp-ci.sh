#!/bin/bash

# 🚨 Replace this with your actual GCP project ID
PROJECT_ID="YOUR_PROJECT_ID"
SERVICE_ACCOUNT_NAME="github-deployer"
EMAIL="$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
KEY_FILE="github-deployer-key.json"

# 1. Set the project
gcloud config set project "$PROJECT_ID"

# 2. Create the service account
gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
  --description="CI/CD deployer for GitHub Actions" \
  --display-name="GitHub Cloud Run Deployer"

# 3. Add IAM roles
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$EMAIL" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$EMAIL" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$EMAIL" \
  --role="roles/iam.serviceAccountUser"

# 4. Generate JSON key
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="$EMAIL"

# 5. Display next steps
echo "✅ Done!"
echo "➡️  Upload the file '$KEY_FILE' to GitHub Secrets as 'GCP_CREDENTIALS'."
echo "   Open: https://github.com/YOUR_USERNAME/medical-assistant/settings/secrets/actions"

