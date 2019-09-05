from praetor.db import engine, sessionmaker, scoped_session
from praetor import crud
from praetor.schemas import NaiveFlow, NaiveFlowRun, NaiveTaskRun

import threading
from dask.distributed import Client, Queue, TimeoutError
import time


class Collector(threading.Thread):
    def __init__(self, dask: str, queue: str = "praetor"):
        super().__init__()
        client = Client(dask)
        self.db = scoped_session(sessionmaker(bind=engine))
        self.queue = Queue(queue, client=client)
        self._stop_signal = threading.Event()

    def run(self):
        while not self._stop_signal.is_set():
            try:
                messages = self.queue.get(batch=True)
                for message in messages:
                    self.process_message(message)
            except TimeoutError:
                pass
            time.sleep(5)

    def process_message(self, message):
        cls = globals()[message.get("cls")]
        obj = message.get("obj")
        if cls is NaiveFlow:
            operation = crud.post_flow
        if cls is NaiveFlowRun:
            operation = crud.post_flow_run
        if cls is NaiveTaskRun:
            operation = crud.post_task_run
        operation(self.db, cls.parse_obj(obj))

    def stop(self):
        self._stop_signal.set()
