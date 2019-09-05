from praetor.models.base import Base
from praetor.models.log_record import LogRecord
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class TaskRun(Base):

    __tablename__ = "task_run"
    __table_args__ = (UniqueConstraint("task_id", "flow_run_id"),)

    state = Column(String)

    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    task = relationship("Task", back_populates="task_runs")
    flow_run_id = Column(Integer, ForeignKey("flow_run.id"), nullable=False)
    flow_run = relationship("FlowRun", back_populates="task_runs")

    log_records = relationship(
        "LogRecord", order_by=LogRecord.log_ts, back_populates="task_run"
    )

    @classmethod
    def ensure(cls, db, task, flow_run, **kwargs):
        return cls.ensure_obj(db, dict(task=task, flow_run=flow_run), **kwargs)
