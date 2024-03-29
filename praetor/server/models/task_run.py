import logging

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from praetor.server.models.base import Base
from praetor.server.models.log_record import LogRecord

logger = logging.getLogger(__name__)


class TaskRun(Base):

    __tablename__ = "task_run"
    __table_args__ = (UniqueConstraint("task_id", "flow_run_id"),)

    state = Column(String)
    map_index = Column(Integer, nullable=False, default=-1)

    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    task = relationship("Task", back_populates="task_runs")
    flow_run_id = Column(Integer, ForeignKey("flow_run.id"), nullable=False)
    flow_run = relationship("FlowRun", back_populates="task_runs")

    # log_records = relationship(
    #     "LogRecord", order_by=LogRecord.log_ts, back_populates="task_run"
    # )

    @classmethod
    def ensure(cls, db, task, flow_run, state=None, map_index=None, **kwargs):
        task_run = cls.ensure_obj(db, dict(task=task, flow_run=flow_run))
        if map_index is not None:
            task_run.map_index = max(task_run.map_index, map_index)
        elif state is not None:
            task_run.state = state
        return task_run
