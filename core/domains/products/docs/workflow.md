# Product Workflow

## States
- DRAFT
- VALIDATED
- PUBLISHED
- UNPUBLISHED
- DELETED

## Transitions
DRAFT → VALIDATED
VALIDATED → PUBLISHED
PUBLISHED → UNPUBLISHED
UNPUBLISHED → PUBLISHED
ANY → DELETED

## Invalid Transitions
- DELETED → ANY
- DRAFT → PUBLISHED (without validation)

## Side Effects
- Publishing triggers search indexing
- Deleting triggers cache eviction
- Unpublishing hides product from buyers
