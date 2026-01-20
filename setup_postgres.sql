-- Setup script for Medical Telegram Warehouse
-- Run this in pgAdmin or psql after installing PostgreSQL

-- Create database if not exists
SELECT 'CREATE DATABASE medical_warehouse'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'medical_warehouse')\gexec

-- Connect to database
\c medical_warehouse;

-- Create schema and table
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name VARCHAR(255),
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    views INTEGER,
    forwards INTEGER,
    image_path TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_channel_name ON raw.telegram_messages(channel_name);
CREATE INDEX IF NOT EXISTS idx_message_date ON raw.telegram_messages(message_date);

-- Create user with permissions (optional)
CREATE USER telegram_user WITH PASSWORD 'telegram_pass';
GRANT CONNECT ON DATABASE medical_warehouse TO telegram_user;
GRANT USAGE ON SCHEMA raw TO telegram_user;
GRANT SELECT, INSERT, UPDATE ON raw.telegram_messages TO telegram_user;

-- Verify setup
SELECT 'PostgreSQL setup complete!' as status;
SELECT COUNT(*) as existing_messages FROM raw.telegram_messages;