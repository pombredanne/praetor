import logging
import signal
import sys
from importlib.util import module_from_spec, spec_from_file_location

from dask.distributed import Queue, get_client, get_worker
from prefect import Flow
from prefect.engine import FlowRunner
from prefect.engine.executors import DaskExecutor

from praetor.client.api import Praetor
from praetor.client.handlers import flow_state_handler, task_state_handler
from praetor.client.shutdown import register_shutdown_signals
from praetor.client.utils import get_run_key
from praetor.schemas import NaiveFlow, NaiveFlowRun, NaiveTaskRun

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
