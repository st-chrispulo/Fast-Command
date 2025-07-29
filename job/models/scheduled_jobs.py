from sqlalchemy import Column, String, Text, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class ScheduledJob(Base):
    __tablename__ = 'tbl_scheduled_jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command = Column(Text, nullable=False)
    payload = Column(JSON, nullable=False)
    cron_expression = Column(Text, nullable=False)
    output_directory = Column(Text)
    enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime)
    next_run_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
