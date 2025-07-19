from commands.base_command import BaseCommand
from pydantic import BaseModel, EmailStr
from auth.db import SessionLocal
from passlib.hash import bcrypt
from fastapi import HTTPException
from sqlalchemy import text


class CreateUserPayload(BaseModel):
    email: EmailStr
    username: str
    password: str


class CreateUserCommand(BaseCommand):
    name = "create_user"
    schema = CreateUserPayload
    require_auth = False

    def run(self, payload: CreateUserPayload):
        db = SessionLocal()
        try:
            existing = db.execute(
                text("SELECT 1 FROM tbl_users WHERE email = :email"),
                {"email": payload.email}
            ).fetchone()

            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")

            hashed_pw = bcrypt.hash(payload.password)

            db.execute(
                text("""
                    INSERT INTO tbl_users (email, username, password_hash)
                    VALUES (:email, :username, :password_hash)
                """),
                {
                    "email": payload.email,
                    "username": payload.username,
                    "password_hash": hashed_pw
                }
            )
            db.commit()
            return {"status": "User created successfully"}
        finally:
            db.close()

