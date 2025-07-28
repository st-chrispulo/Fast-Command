from sqlalchemy import text
from sqlalchemy.orm import Session


def has_permission(db: Session, user_id: int, command: str) -> bool:
    sql = text("""
        SELECT EXISTS (
            SELECT 1
            FROM tbl_user_permissions
            WHERE user_id = :user_id
              AND command_name = :command
        ) AS has_permission;
    """)
    result = db.execute(sql, {"user_id": user_id, "command": command}).scalar()
    return bool(result)
