# Data Ownership

## Owned by Products Domain
- Product identity
- Variants
- Pricing definitions
- Publishing state

## Not Owned
- Inventory quantities → Inventory domain
- Orders → Orders domain
- Payments → Payments domain
- Search indexes → Search service

## Rules
- Other domains may cache product data
- No domain may modify product state directly
- All changes go through Products aggregate
