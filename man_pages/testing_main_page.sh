🏗️ Core Test Blueprint (AliExpress Clone)

Domains: products, orders, payments, cart, users (you can add more easily)
Markers: unit, integration, contract, chaos, saga

1️⃣ Base Folder Structure
core/domains/<domain>/
├── domain/
├── application/
├── adapters/
│   ├── rest/
│   ├── persistence/
│   └── messaging/
├── saga/
├── outbox/
├── read_model/
└── tests/
    ├── domain/           # unit tests
    ├── application/      # use case tests
    ├── adapters/
    │   ├── rest/
    │   ├── persistence/
    │   └── messaging/
    ├── saga/
    ├── outbox/
    └── read_model/


✅ Add __init__.py to every folder so Python treats it as a package.

2️⃣ Pytest Marker Mapping
Marker	Folder	Example File Name	Purpose
unit	tests/domain/	test_product_aggregate.py	Pure domain logic
integration	tests/adapters/rest/	test_product_api.py	API + DB + adapters
contract	tests/contracts/ (optional folder)	test_product_event_schema.py	Event schema / API contracts
chaos	tests/chaos/	test_kafka_down.py	Failure injection / resilience
saga	tests/saga/	test_checkout_saga.py	End-to-end cross-domain workflows

✅ This ensures CI/CD can selectively run tests with pytest -m <marker>.

3️⃣ Example Full Test File Map per Domain
products domain
tests/domain/
├── __init__.py
├── test_product_aggregate.py      # unit
├── test_pricing_policy.py         # unit
├── test_product_status.py         # unit
├── test_variant_generation.py     # unit

tests/application/
├── __init__.py
├── test_create_product.py         # unit/use case
├── test_publish_product.py        # unit/use case
├── test_update_pricing.py         # unit/use case

tests/adapters/rest/
├── __init__.py
├── test_product_api.py            # integration
├── test_serializers.py            # integration

tests/adapters/persistence/
├── __init__.py
├── test_product_repository.py     # integration

tests/adapters/messaging/
├── __init__.py
├── test_product_event_publisher.py # integration

tests/saga/
├── __init__.py
├── test_product_publish_saga.py    # saga

tests/read_model/
├── __init__.py
├── test_product_search_projection.py # unit

tests/outbox/
├── __init__.py
├── test_product_outbox.py           # unit


Repeat the same structure for orders, payments, cart, users — just replace <domain> placeholders in filenames.

4️⃣ Pytest.ini Configuration
[pytest]
markers =
    unit
    integration
    contract
    chaos
    saga


✅ This ensures pytest recognizes all markers without warnings.

5️⃣ Optional Script to Generate Everything
#!/bin/bash
DOMAINS=("products" "orders" "payments" "cart" "users")

for DOMAIN in "${DOMAINS[@]}"; do
  BASE="core/domains/$DOMAIN"

  mkdir -p $BASE/{domain,application,adapters/{rest,persistence,messaging},saga,outbox,read_model,tests/{domain,application,adapters/{rest,persistence,messaging},saga,read_model,outbox}}
  
  # Add __init__.py in every folder
  find $BASE -type d -exec touch {}/__init__.py \;

  # Create example test files
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
done


🚀 Run once and it creates all domains, folders, __init__.py, and test files in one go.

This is a production-ready, repeatable blueprint for a multi-domain DDD + clean architecture project, complete with pytest markers, tests separation, and package initialization.