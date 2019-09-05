from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, and_
from sqlalchemy.orm import relationship
from praetor.models.base import Base
from praetor.models.task import Task
from praetor.models.task_run import TaskRun
from praetor.db import Session


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

    flow = relationship("Flow", back_populates="flow_runs")
    flow_session = relationship("FlowSession", back_populates="flow_runs")

    task_runs = relationship("TaskRun", order_by=TaskRun.id, back_populates="flow_run")

    def ensure_task_run(self, db: Session, task: Task, **kwargs):
        return TaskRun.ensure(db, task=task, flow_run=self, **kwargs)

    def shutdown(self):
        self.state = "Canceled"
        for task_run in self.task_runs:
            if task_run.state not in ("Success", "Failed", "Canceled"):
                task_run.state = "Canceled"

    @classmethod
    def ensure(cls, db: Session, key, flow, flow_session, **kwargs):
        return cls.ensure_obj(
            db, dict(key=key, flow_session=flow_session), flow=flow, **kwargs
        )
