# Role-Based Access Control (RBAC)

## Roles
- Admin
- Seller
- Support
- System

## Permissions
### Admin
- Create, update, delete products
- Publish/unpublish products
- Override validation rules

### Seller
- Create and update own products
- Submit products for publishing
- Cannot delete published products

### Support
- View all products
- Cannot modify product state

### System
- Execute background jobs
- Process outbox events
