


CREATE TABLE dead_letter_events (
    id UUID PRIMARY KEY,
    topic TEXT,
    event_type TEXT,
    payload JSONB,
    retry_count INT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT now()
);
