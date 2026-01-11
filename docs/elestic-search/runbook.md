# 📘 Production Runbook — AliExpress Platform (Kafka + Outbox + Elasticsearch)

> **Audience**: Senior / Staff / Principal Engineers, SREs, On-call
>
> **Scope**: Product domain — Kafka eventing, Outbox, Elasticsearch projections

---

## 1. System Overview

This system follows **DDD + Clean Architecture + CQRS** with **Kafka as the integration backbone**.

### Write Path (Command Side)

```
Client
  → API (Django)
    → Postgres (Domain + Outbox)
      → Outbox Publisher
        → Kafka (product.events)
```

### Read Path (Query Side)

```
Kafka (product.events)
  → Projection Consumers
    → Elasticsearch (Read Models)
```

### Key Guarantees

* Exactly-once *intent* via Outbox
* At-least-once delivery via Kafka
* Idempotent projections
* Replayable read models

---

## 2. Core Components & Responsibilities

### Postgres

* System of record
* Owns domain truth
* Stores Outbox events

### Kafka

* Immutable event log
* Replay source for projections
* Decouples writers & readers

### Elasticsearch

* Read-only query store
* Derived state ONLY
* Never a source of truth

---

## 3. Kafka Topics

| Topic                | Purpose                     |
| -------------------- | --------------------------- |
| `product.events`     | Domain events for products  |
| `dlq.product.events` | Failed events after retries |

---

## 4. Elasticsearch Index Strategy (MANDATORY)

### Rules

1. **Never write to a raw index name**
2. **Always write via alias**
3. **Indices are immutable snapshots**
4. **Rebuild = new index + alias switch**

### Naming Convention

```
product_search_v1_20260110_120045
```

### Alias

```
product_search   → active index
```

---

## 5. Normal Startup Order

### Infrastructure

```bash
docker compose up -d zookeeper kafka db redis elasticsearch
```

### Application

```bash
docker compose up -d api
python manage.py migrate
```

### Runtime

```bash
python manage.py process_outbox
python manage.py run_product_event_consumer
```

---

## 6. Projection Rebuild (Critical Section)

### When to Rebuild

* Elasticsearch schema change
* Projection bug
* ES data corruption
* Backfill requirement

### NEVER Rebuild From

❌ Database
❌ REST APIs
❌ Admin scripts

### ALWAYS Rebuild From

✅ Kafka

---

## 7. Projection Rebuild Command

```bash
python manage.py rebuild_product_search_projection
```

### Internal Steps (Order is STRICT)

1. Create new index with mapping
2. Consume Kafka from offset 0
3. Write into new index ONLY
4. Validate document count
5. Atomically switch alias
6. Stop rebuild consumer

---

## 8. Alias Switch Safety

Alias switch must be **atomic**:

```json
POST /_aliases
{
  "actions": [
    {"remove": {"alias": "product_search", "index": "*"}},
    {"add": {"alias": "product_search", "index": "product_search_v1_xxx"}}
  ]
}
```

✔ Zero downtime
✔ No partial reads

---

## 9. DLQ Handling

### Why DLQ Exists

* Business validation failure
* Schema mismatch
* Non-retriable logic errors

### Process

1. Event retried N times
2. On exhaustion → DLQ
3. DLQ is NOT auto-replayed

### To Inspect

```bash
kafka-console-consumer --topic dlq.product.events
```

---

## 10. Idempotency Rules

All consumers MUST:

* Use aggregate_id as document ID
* Overwrite on replays
* Never assume ordering

This guarantees safe replay.

---

## 11. Operational Checks

### Kafka

```bash
kafka-consumer-groups --describe
```

### Elasticsearch

```bash
GET /_cat/aliases
GET /product_search/_count
```

### Database

```sql
SELECT COUNT(*) FROM outbox_events WHERE processed=false;
```

---

## 12. Incident Scenarios

### ❌ ES Deleted Accidentally

Action:

```bash
rebuild_product_search_projection
```

### ❌ Projection Bug Deployed

Action:

1. Fix code
2. New index version
3. Rebuild

---

## 13. Golden Rules (DO NOT VIOLATE)

* ❌ ES is NOT a source of truth

* ❌ DB must NOT be queried for projections

* ❌ No dual writers

* ❌ No schema-less projections

* ✅ Kafka is replay source

* ✅ Alias-based indices only

* ✅ Rebuilds are disposable

---

## 14. Ownership

| Component      | Owner                    |
| -------------- | ------------------------ |
| Product Events | Product Domain           |
| Projections    | Search / Read Model Team |
| Kafka          | Platform                 |
| ES Cluster     | Platform / SRE           |

---

## 15. Final Principle

> **If you cannot rebuild a read model from Kafka at any time, your architecture is broken.**

This runbook enforces that invariant.

### Projection Rebuild Policy

Source of truth: DATABASE

Kafka is used only for:
- Live updates
- Streaming projections

Kafka MUST NOT be used as the default rebuild source.
