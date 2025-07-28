from sqlalchemy import text
from auth.db import SessionLocal
from logger import logger


def sync_command_registry_to_db(command_registry):
    db = SessionLocal()

    try:
        db.execute(text("TRUNCATE TABLE tbl_commands RESTART IDENTITY CASCADE"))
        for cmd in command_registry:
            db.execute(
                text("""
                    INSERT INTO tbl_commands (name, require_auth, method)
                    VALUES (:name, :require_auth, :method)
                    ON CONFLICT (name) DO NOTHING
                """),
                {
                    "name": cmd.name,
                    "require_auth": getattr(cmd, "require_auth", True),
                    "method": getattr(cmd, "method", "POST")
                }
            )
        db.commit()

        logger.info(f"Synced {len(command_registry)} commands to tbl_commands")


        result = db.execute(
            text("""
                SELECT ur.user_id
                FROM tbl_user_roles ur
                JOIN tbl_roles r ON ur.role_id = r.id
                WHERE r.name = 'super_admin'
            """)
        )
        super_admin_ids = [row[0] for row in result.fetchall()]

        if super_admin_ids:

            db.execute(
                text("DELETE FROM tbl_user_permissions WHERE user_id = ANY(:ids)"),
                {"ids": super_admin_ids}
            )

            commands = db.execute(text("SELECT name FROM tbl_commands")).fetchall()
            for user_id in super_admin_ids:
                for (command_name,) in commands:
                    db.execute(
                        text("""
                            INSERT INTO tbl_user_permissions (user_id, command_name)
                            VALUES (:user_id, :command_name)
                            ON CONFLICT DO NOTHING
                        """),
                        {"user_id": user_id, "command_name": command_name}
                    )

            db.commit()
            logger.info(f"Refreshed permissions for {len(super_admin_ids)} super admins")

    finally:
        db.close()
