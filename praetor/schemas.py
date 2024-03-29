from datetime import datetime
from typing import List

import prefect
from pydantic import BaseModel

from praetor.client.utils import get_run_key


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class Base(OrmModel):

    id: int
    created: datetime
    updated: datetime = None


class NaiveTask(OrmModel):
    """ Naive model means that it's not aware of anything but object's properties
        that are available to Prefect at runtime. Thus, it can be constructed from a Prefect object
        (in this case, Task) and then matched with an existing record in metadata database
        or registered as a new object.
    """

    name: str

    @classmethod
    def from_prefect(cls, task: prefect.Task):
        return cls(name=task.name)


class BaseFlow(OrmModel):

    name: str
    schedule: str = None
    is_online: bool = True


class NaiveEdge(OrmModel):

    upstream_task: NaiveTask
    downstream_task: NaiveTask

    @classmethod
    def from_prefect(cls, edge: prefect.core.Edge):
        return cls(
            upstream_task=edge.upstream_task,
            downstream_task=edge.downstream_task,
            key=edge.key,
        )


class NaiveFlow(BaseFlow):

    tasks: List[NaiveTask] = []
    edges: List[NaiveEdge] = []

    @staticmethod
    def get_schedule(schedule):
        if schedule is None:
            return None
        schedules = []
        for clock in schedule.clocks:
            if hasattr(clock, "cron"):
                schedules.append(clock.cron)
            if hasattr(clock, "interval"):
                schedules.append(str(clock.interval))
        return ", ".join(schedules)

    @classmethod
    def from_prefect(cls, flow: prefect.Flow):
        return cls(
            name=flow.name,
            schedule=cls.get_schedule(flow.schedule),
            is_online=True,
            tasks=[
                NaiveTask.from_prefect(t) for t in flow.tasks if not t.auto_generated
            ],
            edges=[
                NaiveEdge.from_prefect(e)
                for e in flow.edges
                if not (
                    e.downstream_task.auto_generated or e.upstream_task.auto_generated
                )
            ],
        )


class BaseFlowRun(OrmModel):

    key: str
    state: str = None


class NaiveFlowRun(BaseFlowRun):

    flow: BaseFlow


class NaiveTaskRun(OrmModel):

    flow_run: NaiveFlowRun
    task: NaiveTask
    state: str = None
    map_index: int = None

    @classmethod
    def from_prefect(cls, task: prefect.Task, state, map_index=None):
        return cls(
            flow_run=NaiveFlowRun(
                key=get_run_key(), flow=BaseFlow(name=prefect.context.flow_name)
            ),
            task=NaiveTask(name=task.name),
            state=state,
            map_index=map_index,
        )


class FlowTask(Base, NaiveTask):
    pass


class FlowFlowRun(Base, BaseFlowRun):
    pass


class FlowRun(Base, NaiveFlowRun):
    pass


class Flow(Base, BaseFlow):

    recent_flow_runs: List[FlowFlowRun] = []
    flow_runs_states: dict = {}
    tasks_states: dict = {}


class Task(Base, NaiveTask):

    state: str = None


class Edge(Base):

    upstream_task_id: int
    downstream_task_id: int


class TaskRun(Base):

    task_id: int
    state: str
    flow_run: NaiveFlowRun
    map_index: int


class FlowRunDetail(FlowRun):

    task_runs: List[TaskRun]


class FlowDetail(Base, BaseFlow):

    tasks: List[Task]
    edges: List[Edge]
    flow_runs: List[FlowRunDetail] = []


class Message(BaseModel):

    cls: str
    obj: dict
