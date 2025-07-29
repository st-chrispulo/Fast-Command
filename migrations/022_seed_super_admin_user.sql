WITH role_row AS (
    SELECT id FROM tbl_roles WHERE name = 'super_admin'
)
INSERT INTO tbl_user_roles (user_id, role_id)
SELECT 1, id FROM role_row
ON CONFLICT DO NOTHING;