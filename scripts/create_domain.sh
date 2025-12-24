# #!/bin/bash
# DOMAIN=$1

# BASE="core/domains/$DOMAIN"

# mkdir -p \
# $BASE/{domain,application,adapters/{rest,persistence,messaging},saga,outbox,read_model,tests/{domain,application,adapters/{rest,persistence,messaging},saga,read_model,outbox}}

# touch \
# $BASE/tests/domain/test_${DOMAIN}_aggregate.py __init__.py \
# $BASE/tests/domain/test_${DOMAIN}_status.py __init__.py  \
# $BASE/tests/application/test_create_${DOMAIN}.py __init__.py  \
# $BASE/tests/application/test_publish_${DOMAIN}.py __init__.py  \
# $BASE/tests/adapters/rest/test_${DOMAIN}_api.py __init__.py  \
# $BASE/tests/adapters/persistence/test_${DOMAIN}_repository.py __init__.py \
# $BASE/tests/adapters/messaging/test_${DOMAIN}_event_publisher.py __init__.py \
# $BASE/tests/saga/test_${DOMAIN}_publish_saga.py \
# $BASE/tests/read_model/test_${DOMAIN}_search_projection.py __init__.py \
# $BASE/tests/outbox/test_${DOMAIN}_outbox.py __init__.py


#!/bin/bash
set -e

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
  echo "❌ Please provide a domain name"
  echo "Usage: ./create_domain.sh products"
  exit 1
fi

BASE="core/domains/$DOMAIN"

# -----------------------------
# Create folder structure
# -----------------------------
mkdir -p \
$BASE/{domain,application,adapters/{rest,persistence,messaging},saga,outbox,read_model,tests/{domain,application,adapters/{rest,persistence,messaging},saga,read_model,outbox}}

# -----------------------------
# Create __init__.py in ALL dirs
# -----------------------------
find $BASE -type d -exec touch {}/__init__.py \;

# -----------------------------
# Create test files
# -----------------------------
touch \
$BASE/tests/domain/test_${DOMAIN}_aggregate.py \
$BASE/tests/domain/test_${DOMAIN}_status.py \
$BASE/tests/application/test_create_${DOMAIN}.py \
$BASE/tests/application/test_publish_${DOMAIN}.py \
$BASE/tests/adapters/rest/test_${DOMAIN}_api.py \
$BASE/tests/adapters/persistence/test_${DOMAIN}_repository.py \
$BASE/tests/adapters/messaging/test_${DOMAIN}_event_publisher.py \
$BASE/tests/saga/test_${DOMAIN}_publish_saga.py \
$BASE/tests/read_model/test_${DOMAIN}_search_projection.py \
$BASE/tests/outbox/test_${DOMAIN}_outbox.py

echo "✅ Domain '$DOMAIN' created successfully"
