# Products Domain Model

## Aggregate Root
### Product
The Product aggregate is the transactional and consistency boundary.
All business rules related to products must be enforced through it.

## Entities
- Product
- Variant
- Pricing
- Image
- Attribute
- CategoryAssignment

Entities have identity and lifecycle tied to the Product aggregate.

## Value Objects
- Money
- SKU
- Weight
- Dimensions
- ProductStatus

Value objects are immutable and equality-based.

## Domain Events
- ProductCreated
- ProductUpdated
- ProductPublished
- ProductUnpublished
- ProductDeleted

Events represent facts that already happened and are immutable.

## Invariants Summary
- A product must have at least one variant
- A product cannot be published without valid pricing
- Deleted products are immutable
