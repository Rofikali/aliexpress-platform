###6️⃣ Execution Order (This answers your earlier question)
            🔥 THIS ORDER IS LAW 🔥
    1. Create ES mapping
    2. Create physical index (products_v1)
    3. Attach alias (products_search → products_v1)
    4. Run rebuild command
    5. Start consumers
    6. Hit /search API

## Index Alias
    products_search

## Current Version
    products_v1

## Rebuild Steps
    1. Create new index products_v{N}
    2. Run rebuild_product_search_projection
    3. Swap alias atomically
    4. Verify search
    5. Delete old index

## Failure Modes
    - index_not_found_exception → alias missing
    - mapper_parsing_exception → schema mismatch
    - empty results → projection not rebuilt

## Rollback
    - Move alias back to previous index
