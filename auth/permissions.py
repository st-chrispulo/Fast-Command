from sqlalchemy import text
from sqlalchemy.orm import Session


def has_permission(db: Session, user_id: int, command: str) -> bool:
    sql = text("""
        SELECT EXISTS (
            SELECT 1
            FROM tbl_user_roles ur
            JOIN tbl_role_permissions rp ON ur.role_id = rp.role_id
            JOIN tbl_permissions p ON rp.permission_id = p.id
            WHERE ur.user_id = :user_id
              AND p.command = :command
        ) AS has_permission;
    """)
    result = db.execute(sql, {"user_id": user_id, "command": command}).scalar()
    return bool(result)
