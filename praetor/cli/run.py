import signal
import sys
from importlib.util import spec_from_file_location, module_from_spec

from praetor.cli.api import Praetor
from praetor.cli.shutdown import register_shutdown_signals
from praetor.schemas import NaiveFlowRun, NaiveFlow, NaiveTaskRun
from praetor.utils import get_run_key

from prefect import Flow
from prefect.engine.executors import DaskExecutor
from prefect.engine import FlowRunner

from dask.distributed import get_worker, get_client, Queue
import logging


PRAETOR_DEFAULT_URL = "http://localhost:8000/"


class TaskLoggingHandler(logging.Handler):
    def emit(self, record):
        pass


def shutdown_flow(dask, flow: Flow):
    def inner(*_):
        api = Praetor(dask)
        f = NaiveFlow.from_prefect(flow)
        api.shutdown_flow(f)
        sys.exit(0)

    return inner


def flow_state_handler(dask: str):
    def inner(flow, old, new):
        api = Praetor(dask)
        flow_run = NaiveFlowRun(
            key=get_run_key(),
            flow=NaiveFlow.from_prefect(flow),
            state=new.__class__.__name__,
        )
        api.post_flow_run(flow_run)

    return inner


def task_state_handler():
    def inner(task, old, new):
        api = Praetor(client=get_client())
        task_run = NaiveTaskRun.from_prefect(task, state=new.__class__.__name__)
        api.post_task_run(task_run)

    return inner


def import_flow(filename):
    spec = spec_from_file_location("flow", filename)
    f = module_from_spec(spec)
    spec.loader.exec_module(f)
    return f.flow


def run(filename, address=None):
    flow = import_flow(filename)
    executor = DaskExecutor(address=address)
    api = Praetor(address)
    register_shutdown_signals(shutdown_flow(address, flow))
    flow.state_handlers.append(flow_state_handler(address))
    for task in flow.tasks:
        task.state_handlers.append(task_state_handler())
    naive_flow = NaiveFlow.from_prefect(flow)
    api.post_flow(naive_flow)
    try:
        flow.run(executor=executor)
    finally:
        api.shutdown_flow(naive_flow)
        api.close()
        sys.exit(0)
