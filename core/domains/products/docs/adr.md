# Architecture Decision Records

## ADR-001: DDD Aggregate Root
Decision: Use Product as Aggregate Root  
Reason: Strong consistency and rule enforcement

## ADR-002: CQRS
Decision: Separate write and read models  
Reason: Read-heavy access patterns and scalability

## ADR-003: Event-Driven Integration
Decision: Use Kafka for domain events  
Reason: Loose coupling and scalability

## ADR-004: Outbox Pattern
Decision: Publish events via DB-backed outbox  
Reason: Prevent dual-write and data loss

## ADR-005: Framework-Free Domain
Decision: Domain layer has no Django/Kafka imports  
Reason: Testability and longevity
