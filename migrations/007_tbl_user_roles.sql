CREATE TABLE IF NOT EXISTS tbl_user_roles (
    user_id INTEGER REFERENCES tbl_users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES tbl_roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

