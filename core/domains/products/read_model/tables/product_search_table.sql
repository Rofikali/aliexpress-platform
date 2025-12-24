CREATE TABLE IF NOT EXISTS product_search (
    id UUID PRIMARY KEY,
    name TEXT,
    description TEXT,
    category_id UUID,
    price NUMERIC,
    status TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
