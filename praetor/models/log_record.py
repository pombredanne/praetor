from praetor.models.base import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class LogRecord(Base):

    __tablename__ = "log_record"

    log_ts = Column(DateTime, nullable=False)
    logger_name = Column(String(128), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String(10000), nullable=False)
    task_run_id = Column(Integer, ForeignKey("task_run.id"))

    task_run = relationship("TaskRun", back_populates="log_records")
