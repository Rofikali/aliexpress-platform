# Products Domain Invariants

## Product Lifecycle
1. Products start in DRAFT state
2. Only DRAFT or UNPUBLISHED products may be edited
3. Only VALIDATED products may be PUBLISHED
4. DELETED products are immutable

## Pricing Rules
- Price must be greater than zero
- Currency must be supported
- Every published product must have pricing

## Variants
- At least one variant is required
- SKU must be unique per product
- Variants cannot exist without a product

## Images
- At least one image is required for publishing
- Image URLs must be valid and reachable

## Events
- Every state change emits a domain event
- Events must be published via outbox
- No direct Kafka publishing from domain layer
