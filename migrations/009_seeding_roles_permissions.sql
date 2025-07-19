-- Insert roles
INSERT INTO tbl_roles (name, description)
VALUES
  ('admin', 'Administrator with full access'),
  ('viewer', 'Can view data only');

-- Insert permissions
INSERT INTO tbl_permissions (command, description)
VALUES
  ('user_create', 'Create a new user'),
  ('network_assign_ip', 'Assign static IPs to a network');

-- Map admin to all permissions
INSERT INTO tbl_role_permissions (role_id, permission_id)
SELECT
  r.id, p.id
FROM
  tbl_roles r, tbl_permissions p
WHERE
  r.name = 'admin';
