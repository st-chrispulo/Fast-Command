from sqlalchemy import Column, String, Text, JSON, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime, timezone

Base = declarative_base()


class QueuedJob(Base):
    __tablename__ = 'tbl_queued_jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command = Column(Text, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    output_directory = Column(Text)
    result = Column(JSON)
    error_message = Column(Text)
    attempts = Column(Integer, default=0)

    scheduled_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
