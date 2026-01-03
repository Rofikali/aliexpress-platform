# Failure Scenarios

## Kafka Unavailable
- Outbox continues accumulating events
- No data loss
- Processor retries automatically

## Duplicate Events
- Consumers must be idempotent
- Event keys enforce deduplication

## Partial Failures
Example:
- Product published
- Search indexing fails

Mitigation:
- Retry via consumer
- Rebuild read model if necessary

## Data Corruption
- Rebuild read models from write DB
- Domain remains source of truth
