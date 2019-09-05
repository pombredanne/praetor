from praetor.models.base import Base

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Edge(Base):

    __tablename__ = "edge"
    __table_args__ = (UniqueConstraint("upstream_task_id", "downstream_task_id"),)

    flow_id = Column(Integer, ForeignKey("flow.id"), nullable=False)
    flow_session_id = Column(Integer, ForeignKey("flow_session.id"), nullable=False)
    upstream_task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    downstream_task_id = Column(Integer, ForeignKey("task.id"), nullable=False)

    flow = relationship("Flow")
    flow_session = relationship("FlowSession", back_populates="edges")
    upstream_task = relationship(
        "Task", foreign_keys=upstream_task_id, back_populates="edges_out"
    )
    downstream_task = relationship(
        "Task", foreign_keys=downstream_task_id, back_populates="edges_in"
    )

    @classmethod
    def ensure(cls, db, flow, upstream_task, downstream_task, **kwargs):
        return super().ensure_obj(
            db,
            dict(
                flow=flow, upstream_task=upstream_task, downstream_task=downstream_task
            ),
            **kwargs
        )
