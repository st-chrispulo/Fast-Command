CREATE TABLE IF NOT EXISTS tbl_role_permissions (
    role_id INTEGER REFERENCES tbl_roles(id) ON DELETE CASCADE,
    permission_id INTEGER REFERENCES tbl_permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);
