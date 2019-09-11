import prefect
from praetor.cli.client import LocalPraetorClient, DaskPraetorClient
from praetor.cli.handlers import flow_state_handler, task_state_handler
from praetor import schemas

from dask.distributed import get_client
from toolz import curry


class NaiveMixin:

    naive_cls = None

    @property
    def naive(self):
        return self.naive_cls.from_prefect(self)


class Flow(NaiveMixin, prefect.Flow):

    naive_cls = schemas.NaiveFlow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state_handlers.append(flow_state_handler)

    def run(self, *args, **kwargs):
        client = self.get_client(kwargs.get("executor"))
        try:
            self.report_online(client)
            super().run(*args, **kwargs)
        finally:
            self.report_offline(client)

    def get_client(self, executor=None):
        try:
            return DaskPraetorClient(client=get_client())
        except ValueError:
            if isinstance(executor, prefect.engine.executors.DaskExecutor):
                return DaskPraetorClient(address=executor.address)
        return LocalPraetorClient()

    def report_online(self, client):
        flow = self.naive
        flow.is_online = True
        client.send(flow)

    def report_offline(self, client):
        flow = self.naive
        flow.is_online = False
        client.send(flow)


class Task(prefect.Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state_handlers.append(task_state_handler)


@curry
def task(fn, **kwargs):
    result = prefect.task(fn, **kwargs)
    result.state_handlers.append(task_state_handler)
    return result
