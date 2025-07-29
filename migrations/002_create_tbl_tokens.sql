CREATE TABLE IF NOT EXISTS tbl_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES tbl_users(id) ON DELETE CASCADE,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    scope TEXT,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

