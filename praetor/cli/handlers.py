from dask.distributed import get_client
from prefect import context as ctx

from praetor import schemas
from praetor.cli.client import DaskPraetorClient, LocalPraetorClient
from praetor.utils import get_run_key


def decide_client():
    try:
        return DaskPraetorClient(client=get_client())
    except ValueError:
        return LocalPraetorClient()


def flow_state_handler(flow, old, new):
    flow_run = schemas.NaiveFlowRun(
        key=get_run_key(), flow=flow.naive, state=new.__class__.__name__
    )
    client = decide_client()
    client.send(flow_run)


def task_state_handler(task, old, new):
    task_run = schemas.NaiveTaskRun.from_prefect(
        task, state=new.__class__.__name__, map_index=ctx.map_index
    )
    client = decide_client()
    client.send(task_run)
