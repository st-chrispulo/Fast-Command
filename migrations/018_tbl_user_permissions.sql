CREATE TABLE IF NOT EXISTS tbl_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES tbl_users(id) ON DELETE CASCADE,
    command_name TEXT NOT NULL,
    granted_at TIMESTAMP DEFAULT NOW(),
    granted_by INTEGER REFERENCES tbl_users(id) ON DELETE SET NULL,
    UNIQUE (user_id, command_name)
);
