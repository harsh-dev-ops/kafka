CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    sender_name VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);