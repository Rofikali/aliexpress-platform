# Product Search Projection – Runbook

## Purpose

This runbook describes how to rebuild and operate the Product Search projection
backed by Elasticsearch and Kafka.

---

## Architecture Overview

- Source of truth: Kafka `product.events`
- Projection: Elasticsearch
- Read alias: `product_search_current`

---

## Normal Operation

- Live consumer group: `product-search-consumer`
- Writes always go to alias
- Index versioning enabled

---

## Rebuild Procedure (Zero Downtime)

### Preconditions

- Kafka healthy
- Elasticsearch healthy
- No pending schema migrations

### Steps

1. Run rebuild command
2. Validate new index
3. Switch alias
4. Monitor error rate

---

## Rollback Procedure

1. Switch alias back to previous index
2. Restart consumer
3. Investigate failure

---

## Failure Scenarios

### Rebuild hangs

Cause:

- Infinite Kafka consumer used

Fix:

- Use finite replay consumer

---

### Duplicate documents

Cause:

- Consumer group reused

Fix:

- Disable consumer groups for rebuild

---

## Monitoring & Alerts

- Consumer lag
- Elasticsearch indexing latency
- Alias health

---

## Ownership

- Team: Search Platform
- Slack: #search-oncall
