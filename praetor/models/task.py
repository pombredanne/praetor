from praetor.models.base import Base
from praetor.models.task_run import TaskRun
from praetor.models.edge import Edge

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Task(Base):

    __tablename__ = "task"
    __table_args__ = (UniqueConstraint("name", "flow_id"),)

    name = Column(String(32), nullable=False)
    flow_id = Column(Integer, ForeignKey("flow.id"), nullable=False)

    flow = relationship("Flow", back_populates="tasks")
    task_runs = relationship(
        "TaskRun",
        order_by=TaskRun.id,
        back_populates="task",
        cascade="save-update, delete",
    )
    edges_in = relationship(
        "Edge",
        foreign_keys=Edge.downstream_task_id,
        order_by=Edge.id,
        back_populates="downstream_task",
        cascade="save-update, delete",
    )
    edges_out = relationship(
        "Edge",
        foreign_keys=Edge.upstream_task_id,
        order_by=Edge.id,
        back_populates="upstream_task",
        cascade="save-update, delete",
    )

    @classmethod
    def ensure(cls, db, name, flow, **kwargs):
        return cls.ensure_obj(db, dict(name=name), flow=flow, **kwargs)

    @property
    def state(self):
        return self.task_runs[-1].state if len(self.task_runs) > 0 else None
