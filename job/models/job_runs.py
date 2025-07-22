from sqlalchemy import Column, String, Text, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class JobRun(Base):
    __tablename__ = 'tbl_job_runs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), nullable=False)
    job_type = Column(String, nullable=False)
    command = Column(Text, nullable=False)
    payload = Column(JSON, nullable=False)
    output_directory = Column(Text)
    result = Column(JSON)
    error_message = Column(Text)
    status = Column(String, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
