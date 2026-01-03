# Products Domain

## Purpose
The Products domain is responsible for managing the full lifecycle of products
listed on the platform. It defines product identity, structure, pricing,
variants, and publishability.

This domain is the **single source of truth** for product state.

## Responsibilities
- Create and update products
- Manage variants and attributes
- Apply pricing rules
- Control publish/unpublish lifecycle
- Emit product-related domain events

## Explicit Non-Responsibilities
This domain does NOT own:
- Inventory stock levels (Inventory domain)
- Checkout flows (Checkout domain)
- Payments (Payments domain)
- Search infrastructure (read-model only)
- Reviews and moderation decisions (Moderation service)

## Architecture
- Domain-Driven Design (DDD)
- Aggregate Root: Product
- CQRS (Write Model + Read Model)
- Event-driven integration (Kafka)
- Outbox pattern for guaranteed event delivery

## Entry Points
- REST APIs
- Admin UI
- Kafka consumers (reactive updates)

## Exit Points
- Kafka domain events
- Read-model projections
- Cache updates
