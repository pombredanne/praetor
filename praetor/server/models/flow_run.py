import logging

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, and_
from sqlalchemy.orm import relationship

from praetor.server.db import Session
from praetor.server.models.base import Base
from praetor.server.models.task import Task
from praetor.server.models.task_run import TaskRun

FINAL_STATES = ["Success", "Failed", "Canceled", "Mapped"]

logger = logging.getLogger(__name__)


class FlowRun(Base):

    __tablename__ = "flow_run"
    __table_args__ = (
        UniqueConstraint("key", "flow_session_id"),
        UniqueConstraint("key", "flow_id"),
    )

    key = Column(String(64), nullable=False)
    state = Column(String)

    flow_id = Column(Integer, ForeignKey("flow.id"), nullable=False)
    flow_session_id = Column(Integer, ForeignKey("flow_session.id"), nullable=False)

    flow = relationship("Flow")
    flow_session = relationship("FlowSession", back_populates="flow_runs")

    task_runs = relationship("TaskRun", order_by=TaskRun.id, back_populates="flow_run")

    @property
    def tasks(self):
        return {task_run.task for task_run in self.task_runs}

    def ensure_task_run(self, db: Session, task: Task, **kwargs):
        return TaskRun.ensure(db, task=task, flow_run=self, **kwargs)

    def shutdown(self):
        if self.state not in FINAL_STATES:
            self.state = "Canceled"
            for task_run in self.task_runs:
                if task_run.state not in FINAL_STATES:
                    task_run.state = "Canceled"

    @classmethod
    def ensure(cls, db: Session, key, flow, flow_session, **kwargs):
        return cls.ensure_obj(
            db, dict(key=key, flow_session=flow_session), flow=flow, **kwargs
        )
