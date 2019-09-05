from sqlalchemy import Column, String, Boolean, and_
from sqlalchemy.orm import relationship

from praetor.models.base import Base
from praetor.models.task import Task
from praetor.models.flow_run import FlowRun
from praetor.models.flow_session import FlowSession

from collections import defaultdict


class Flow(Base):

    __tablename__ = "flow"

    name = Column(String(32), nullable=False, unique=True)
    description = Column(String)
    is_online = Column(Boolean, default=False)
    schedule = Column(String(512))

    flow_sessions = relationship(
        "FlowSession",
        order_by=FlowSession.id,
        back_populates="flow",
        lazy="dynamic",
        cascade="save-update, delete",
    )
    flow_runs = relationship(
        "FlowRun",
        order_by=FlowRun.id,
        back_populates="flow",
        lazy="dynamic",
        cascade="save-update, delete",
    )

    def shutdown(self):
        self.is_online = False
        if self.latest_session:
            self.latest_session.shutdown()

    @property
    def recent_flow_runs(self):
        return self.flow_runs[-10:]

    @property
    def flow_runs_states(self):
        result = defaultdict(lambda: 0)
        for run in self.flow_runs:
            result[run.state] += 1
        return result

    @property
    def tasks_states(self):
        result = defaultdict(lambda: 0)
        for task_run in self.latest_session.latest_flow_run.task_runs:
            result[task_run.state] += 1
        return result

    @property
    def latest_session(self):
        return self.flow_sessions[-1] if self.flow_sessions.count() > 0 else None

    @property
    def tasks(self):
        sess = self.latest_session
        if sess is not None:
            return sess.tasks
        return []

    @property
    def edges(self):
        sess = self.latest_session
        if sess is not None:
            return sorted(
                sess.edges, key=lambda e: (e.upstream_task.id, e.downstream_task.id)
            )
        return []

    @classmethod
    def ensure(cls, db, name, **kwargs):
        return cls.ensure_obj(db, dict(name=name), **kwargs)

    def create_session(self, db, tasks=None, edges=None):
        for flow_run in db.query(FlowRun).filter(
            and_(FlowRun.flow == self, FlowRun.state.notin_(["Success", "Failed"]))
        ):
            flow_run.shutdown()  # shutdown all unfinished runs in previous sessions
        db.commit()
        flow_session = FlowSession.create(db, flow=self)
        db.commit()
        for index, task in enumerate(tasks or []):
            flow_session.ensure_task(db, task.name, index=index)
        db.commit()
        for edge in edges or []:
            upstream = flow_session.ensure_task(db, edge.upstream_task.name)
            downstream = flow_session.ensure_task(db, edge.downstream_task.name)
            flow_session.ensure_edge(
                db, upstream_task=upstream, downstream_task=downstream
            )
