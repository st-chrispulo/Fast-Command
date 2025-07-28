INSERT INTO tbl_roles (name)
VALUES ('super_admin')
ON CONFLICT (name) DO NOTHING;