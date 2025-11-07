#!/bin/bash

# Function to get env var from .env file
get_env_var() {
  local var_name=$1
  grep -v '^#' .env | grep "^${var_name}=" | cut -d '=' -f 2-
}

# Get values from .env
VM_NAME=$(get_env_var "VM_NAME")
PROJECT_ID=$(get_env_var "PROJECT_ID")
ZONE=$(get_env_var "ZONE")

# Validate that vars were found
if [ -z "$VM_NAME" ] || [ -z "$PROJECT_ID" ] || [ -z "$ZONE" ]; then
  echo "Error: Missing required environment variables in .env"
  exit 1
fi

# Get absolute path to project root
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Files and directories to push
FILES_TO_PUSH=(
  "$PROJECT_ROOT/thesis.pdf"
  "$PROJECT_ROOT/index.html"
  "$PROJECT_ROOT/output/data"
  "$PROJECT_ROOT/output/maps"
)

# Validate that all required files/directories exist
for item in "${FILES_TO_PUSH[@]}"; do
  if [ ! -e "$item" ]; then
    echo "Error: Required file or directory not found: $item"
    exit 1
  fi
done

# Create temp directory structure on remote VM
gcloud compute ssh "$VM_NAME" \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  -- mkdir -p /tmp/html-upload/output/

# Push thesis.pdf and index.html
gcloud compute scp \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  "$PROJECT_ROOT/thesis.pdf" \
  "$PROJECT_ROOT/index.html" \
  "$VM_NAME":/tmp/html-upload/

# Push output/data directory
gcloud compute scp \
  --recurse \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  "$PROJECT_ROOT/output/data" \
  "$VM_NAME":/tmp/html-upload/output/

# Push output/maps directory
gcloud compute scp \
  --recurse \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  "$PROJECT_ROOT/output/maps" \
  "$VM_NAME":/tmp/html-upload/output/

# Move files to /var/www/html with sudo
gcloud compute ssh "$VM_NAME" \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  -- sudo rsync -a --delete /tmp/html-upload/ /var/www/html/thesis/

echo "Successfully pushed thesis files to $VM_NAME:/var/www/html/thesis/"