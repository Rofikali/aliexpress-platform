🧱 Domain Scaffolding Tool

Clean Architecture · DDD · Hexagonal · Event-Driven

This project includes a small but powerful shell script that automatically creates a full Domain-Driven Design (DDD) folder structure for new domains such as products, orders, or payments.

It enforces clean boundaries, test isolation, and long-term scalability.

📦 What This Tool Does

Running a single command creates:

A DDD-aligned domain structure

Separate layers for:

Domain logic

Application use cases

Adapters (REST, persistence, messaging)

Saga, Outbox, Read Models

A complete test layout

__init__.py in every folder (Python-safe)

Ready-to-write test files

All in one command.

🚀 Quick Start
1️⃣ Make the script executable (once)
chmod +x scripts/create_domain.sh

2️⃣ Create a new domain
./scripts/create_domain.sh products
./scripts/create_domain.sh orders
./scripts/create_domain.sh payments


That’s it.
Your domain is ready.

🗂️ Generated Folder Structure

Example for products:

core/domains/products/
├── domain/                # Pure business rules (NO Django, NO DB)
├── application/           # Use cases / commands / handlers
├── adapters/
│   ├── rest/              # API controllers, serializers
│   ├── persistence/       # ORM / repositories
│   └── messaging/         # Kafka / events / publishers
├── saga/                  # Long-running workflows
├── outbox/                # Transactional event outbox
├── read_model/            # Projections / search models
│
├── tests/
│   ├── domain/            # Business rule tests
│   ├── application/       # Use case tests
│   ├── adapters/
│   │   ├── rest/
│   │   ├── persistence/
│   │   └── messaging/
│   ├── saga/
│   ├── read_model/
│   └── outbox/


Every directory contains an __init__.py, so Python always recognizes it as a package.

🧠 Why This Structure Exists
❌ What we avoid

Fat Django apps

Business logic in views

Tight DB coupling

Un-testable code

Rewrite after 1 year

✅ What we enforce

Pure domain logic

Explicit use cases

Framework isolation

Event-driven scalability

Testability at every layer

This structure works for:

1 developer

50 developers

500 developers

10+ years of evolution

🧪 Testing Philosophy

Each layer has its own tests:

Layer	What is tested
domain	Rules, invariants, state transitions
application	Use cases, workflows
adapters	IO, API, DB integration
saga	Multi-step business flows
outbox	Event persistence & publishing
read_model	Projections & queries

No layer tests another layer’s internals.

🧑‍🎓 For Juniors

If you’re new:

Start in domain/

Write business rules first

Tests go in tests/domain/

No Django imports allowed there

If you can explain your domain logic without mentioning Django — you’re doing it right.

🧑‍💼 For Seniors / Staff

This layout supports:

Hexagonal Architecture

Event Sourcing (future-ready)

CQRS

Saga orchestration

Outbox pattern

Multi-DB setups

It is safe for:

Kafka

Elasticsearch

Microservices (if needed later)

🛠 Script Internals (FYI)

The script:

Uses mkdir -p for atomic folder creation

Uses find … -type d to add __init__.py everywhere

Generates standard test file names automatically

No manual work. No copy-paste.

🧾 Example Command Flow
./scripts/create_domain.sh products
# → Creates core/domains/products/**

./scripts/create_domain.sh orders
# → Creates core/domains/orders/**

./scripts/create_domain.sh payments
# → Creates core/domains/payments/**

🏁 Final Note

This tool is not about speed.

It’s about:

Clarity

Discipline

Longevity

“Good architecture feels boring on day one and brilliant on day 1000.”

You’re building it the right way.