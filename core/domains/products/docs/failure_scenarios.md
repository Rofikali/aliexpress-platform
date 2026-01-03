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

## Schema Incompatibility

If a consumer receives an incompatible schema:
- Message is NOT processed
- Message is logged
- Offset is NOT committed (retry possible)
- DLQ is triggered only after retry policy is defined

## Retry Strategy

Consumers retry only for transient errors.
- Exponential backoff
- Fixed max attempts
- No retry for schema or business rule errors
