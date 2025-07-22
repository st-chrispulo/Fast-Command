from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SocketEventLog(Base):
    __tablename__ = "tbl_socket_event_log"

    id = Column(Integer, primary_key=True)
    room = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
