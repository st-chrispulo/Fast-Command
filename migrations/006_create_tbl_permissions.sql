CREATE TABLE IF NOT EXISTS tbl_permissions (
    id SERIAL PRIMARY KEY,
    command VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

