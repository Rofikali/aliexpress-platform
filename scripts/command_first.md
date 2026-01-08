# Operations Commands — Kafka, Outbox, Consumers, Replay

This file is a **single reference** for running services in **long-running (daemon)** mode and **short/manual (one-shot)** mode.

Scope:

* Django API
* Outbox Publisher
* Kafka Consumers
* Replay / Rewind
* Health & Debug

---

## 1️⃣ Long‑Running Services (Daemon / Production Style)

These are meant to run **continuously** (Docker service, systemd, K8s Deployment).

### API Service

```bash
# Start Django API (gunicorn / uvicorn in real prod)
docker compose up api
```

### Kafka Broker

```bash
# Kafka + Zookeeper (or KRaft)
docker compose up kafka
```

### Outbox Publisher (Dedicated Service)

```bash
# Continuous polling of outbox table
docker compose up outbox-publisher
```

Purpose:

* Reads DB outbox rows
* Builds event envelope
* Publishes to Kafka
* Marks rows as SENT

---

### Product Event Projection Consumer (Read Model)

```bash
# Long-running consumer
docker compose up product-event-consumer
```

Consumes:

* product.events

Updates:

* Elasticsearch / read tables

---

### Product Command Consumer (Write Side / Saga)

```bash
# Command-side consumer
docker compose up product-command-consumer
```

Consumes:

* product.commands

---

## 2️⃣ Short / Manual / One‑Shot Commands

These are **intentional, explicit executions**.
Used for:

* backfills
* debugging
* admin operations

---

### Run Outbox Once (Manual Flush)

```bash
docker compose exec api python manage.py process_outbox
```

Use when:

* Testing event publishing
* Debugging envelope / routing

---

### Run Product Event Consumer Manually

```bash
docker compose exec api python manage.py run_product_event_consumer
```

Use when:

* Debugging consumer logic
* Testing projection code

---

### Run Product Command Consumer Manually

```bash
docker compose exec api python manage.py run_product_consumer
```

---

## 3️⃣ Kafka Inspection & Debug Commands

### List Consumer Groups

```bash
docker exec -it aliexpress_kafka \
  kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --list
```

---

### Describe Consumer Group (Lag / Offsets)

```bash
docker exec -it aliexpress_kafka \
  kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --group product-event-projection-group \
  --describe
```

---

### Watch Lag Continuously

```bash
watch -n 2 "docker exec -it aliexpress_kafka \
  kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --group product-event-projection-group \
  --describe"
```

---

## 4️⃣ Replay / Rewind (STAFF‑GRADE SAFE WAY)

### Rewind Consumer Group to Beginning

```bash
docker exec -it aliexpress_kafka \
  kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --group product-event-projection-group \
  --topic product.events \
  --reset-offsets --to-earliest --execute
```

Rules:

* ONLY for read‑model consumers
* NEVER for command consumers
* Projections MUST be idempotent

---

### Rewind to Specific Offset

```bash
docker exec -it aliexpress_kafka \
  kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --group product-event-projection-group \
  --topic product.events:0 \
  --reset-offsets --to-offset 1200 --execute
```

---

## 5️⃣ DLQ Operations

### Consume DLQ Manually

```bash
docker exec -it aliexpress_kafka \
  kafka-console-consumer \
  --bootstrap-server aliexpress_kafka:9092 \
  --topic dlq.product.events \
  --from-beginning
```

---

### Replay DLQ (Manual Re‑publish)

```bash
python scripts/replay_dlq.py --topic dlq.product.events --target product.events
```

Rule:

* Requires idempotent handlers
* Must preserve original event_id

---

## 6️⃣ Health & Observability

### API Health

```bash
curl http://localhost:8000/health/
```

---

### Metrics

```bash
curl http://localhost:8000/metrics
```

---

### Kafka Topics

```bash
docker exec -it aliexpress_kafka \
  kafka-topics \
  --bootstrap-server aliexpress_kafka:9092 \
  --list
```

---

## 7️⃣ Kill / Restart (Safe Ops)

### Restart Consumer

```bash
docker compose restart product-event-consumer
```

### Stop Everything

```bash
docker compose down
```

---

## 🧠 Final Notes (NON‑NEGOTIABLE)

* Outbox publisher is **not Celery**
* Consumers are **stateless + replayable**
* Read models are **rebuildable anytime**
* Command consumers are **never rewound**

This file is safe to hand to:

* New engineers
* On‑call SREs
* Incident response

If a command is not here → it should not be run.
