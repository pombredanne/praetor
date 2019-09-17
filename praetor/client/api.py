from requests_toolbelt.sessions import BaseUrlSession, urljoin
from requests import ConnectionError
from prefect import Flow
from praetor.schemas import Base, NaiveFlow, NaiveFlowRun, NaiveTaskRun
import logging
import os
import json

from dask.distributed import Client, Queue


class Praetor:
    def __init__(self, dask=None, client=None, logger=None):
        if dask is None and client is None:
            dask = "tcp://localhost:8786"
        if client is None:
            client = Client(address=dask)
        if logger is None:
            self.logger = logging.getLogger("praetor")
        else:
            self.logger = logger
        self.queue = Queue("praetor", client=client)

    def obj_to_message(self, obj):
        mapping = dict(
            NaiveFlow="flows/", NaiveFlowRun="flow_runs/", NaiveTaskRun="task_runs/"
        )
        return dict(
            cls=obj.__class__.__name__,
            endpoint=mapping[obj.__class__.__name__],
            obj=obj.dict(),
        )

    def post_flow(self, flow: NaiveFlow):
        self.queue.put(self.obj_to_message(flow), timeout=3)

    def shutdown_flow(self, flow: NaiveFlow):
        flow.is_online = False
        self.queue.put(self.obj_to_message(flow), timeout=3)

    def post_flow_run(self, flow_run: NaiveFlowRun):
        self.queue.put(self.obj_to_message(flow_run), timeout=3)

    def post_task_run(self, task_run: NaiveTaskRun):
        self.queue.put(self.obj_to_message(task_run), timeout=3)

    def close(self):
        self.queue.close()
        self.queue.client.close()
