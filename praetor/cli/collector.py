from praetor.db import engine, sessionmaker, scoped_session, Session
from praetor import crud
from praetor.schemas import NaiveFlow, NaiveFlowRun, NaiveTaskRun

import logging
import threading
from dask.distributed import Client, Queue, TimeoutError
import time
from contextlib import closing


def process_message(db, message):
    logger = logging.getLogger(__name__)
    logger.debug(f"Processing message: {message.get('cls')}")
    cls = globals()[message.get("cls")]
    obj = message.get("obj")
    if cls is NaiveFlow:
        operation = crud.post_flow
    if cls is NaiveFlowRun:
        operation = crud.post_flow_run
    if cls is NaiveTaskRun:
        operation = crud.post_task_run
    operation(db, cls.parse_obj(obj))


class PraetorCollector(threading.Thread):
    def __init__(self):
        self._stop_signal = threading.Event()
        super().__init__()

    def stop(self):
        self._stop_signal.set()

    def run(self):
        logger = logging.getLogger(__name__)
        while not self._stop_signal.is_set():
            with closing(Session()) as db:
                for message in self.receive_messages():
                    try:
                        process_message(db, message)
                    except Exception as e:
                        logger.error(e)
            time.sleep(1)

    def receive_messages(self):
        raise NotImplementedError


class DaskPraetorCollector(PraetorCollector):
    def __init__(self, address):
        client = Client(address)
        self.queue = Queue("praetor", client=client)
        super().__init__()

    def receive_messages(self):
        return self.queue.get(timeout=1, batch=True)
