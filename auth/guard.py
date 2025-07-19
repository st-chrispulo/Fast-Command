from auth.permissions import has_permission
from auth.db import SessionLocal
from fastapi import HTTPException, status


def check_permission(user_id: int, command: str):
    db = SessionLocal()
    try:
        if not has_permission(db, user_id, command):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for '{command}'"
            )
    finally:
        db.close()
