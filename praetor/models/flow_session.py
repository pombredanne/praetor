from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from praetor.models.base import Base
from praetor.models.edge import Edge
from praetor.models.flow_run import FlowRun
from praetor.models.task import Task
from praetor.models.task_run import TaskRun


class FlowSession(Base):

    __tablename__ = "flow_session"

    flow_id = Column(Integer, ForeignKey("flow.id"), nullable=False)

    flow = relationship("Flow", back_populates="flow_sessions")
    flow_runs = relationship(
        "FlowRun", order_by=FlowRun.id, back_populates="flow_session"
    )
    tasks = relationship(
        "Task", back_populates="flow_session", cascade="save-update, delete"
    )
    edges = relationship(
        "Edge", back_populates="flow_session", cascade="save-update, delete"
    )

    @property
    def latest_flow_run(self):
        return self.flow_runs[-1] if len(self.flow_runs) > 0 else None

    def ensure_task(self, db, name, **kwargs):
        return Task.ensure(db, name=name, flow=self.flow, flow_session=self, **kwargs)

    def ensure_edge(self, db, upstream_task, downstream_task):
        return Edge.ensure(
            db,
            flow_session=self,
            upstream_task=upstream_task,
            downstream_task=downstream_task,
            flow=self.flow,
        )

    def ensure_flow_run(self, db, key, **kwargs):
        return FlowRun.ensure(db, key=key, flow_session=self, flow=self.flow, **kwargs)

    def shutdown(self):
        if self.latest_flow_run:
            self.latest_flow_run.shutdown()
