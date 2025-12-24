#!/bin/bash
# Test script for create_domain.sh

echo "Testing create_domain.sh script..."

# Temporary domain name for testing
TEST_DOMAIN="testdomain"

# Run the original script
./scripts/create_domain.sh $TEST_DOMAIN

# Check if the main folders were created
FOLDERS=("domain" "application" "adapters" "adapters/rest" "adapters/persistence" "adapters/messaging" "saga" "outbox" "read_model" "tests")

BASE="core/domains/$TEST_DOMAIN"

SUCCESS=true

for folder in "${FOLDERS[@]}"; do
  if [ ! -d "$BASE/$folder" ]; then
    echo "❌ Folder missing: $BASE/$folder"
    SUCCESS=false
  else
    echo "✅ Folder exists: $BASE/$folder"
  fi
done

# Check if sample test file exists
TEST_FILE="$BASE/tests/domain/test_${TEST_DOMAIN}_aggregate.py"
if [ -f "$TEST_FILE" ]; then
  echo "✅ Test file exists: $TEST_FILE"
else
  echo "❌ Test file missing: $TEST_FILE"
  SUCCESS=false
fi

if [ "$SUCCESS" = true ]; then
  echo "🎉 All folders and files created successfully!"
else
  echo "⚠️ Some folders/files are missing."
fi

# Optional: clean up after test
# rm -rf "$BASE"
