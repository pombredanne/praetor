from prefect import Flow
from praetor.schemas import Base, NaiveFlow, NaiveFlowRun, NaiveTaskRun

from requests_toolbelt.sessions import BaseUrlSession, urljoin
from requests import ConnectionError
import logging
import os
import json

from dask.distributed import Client, Queue
from contextlib import redirect_stdout
from os import devnull

import multiprocessing


class PraetorClient:
    def obj_to_message(self, obj):
        return dict(cls=obj.__class__.__name__, obj=obj.dict())

    def send(self, obj):
        self.send_message(self.obj_to_message(obj))

    def send_message(self, message):
        raise NotImplementedError


class LocalPraetorClient(PraetorClient):
    def __init__(self):
        self.session = BaseUrlSession(base_url="http://127.0.0.1:8000/api/")

    def send_message(self, message):
        self.session.post("message/", json=message)


class DaskPraetorClient(PraetorClient):
    def __init__(self, address=None, client=None):
        if (client or address) is None:
            raise ValueError("address or client must be provided")
        client = Client(address) if address is not None else client
        self.queue = Queue("praetor", client=client)

    def send_message(self, message):
        logger = logging.getLogger(__name__)
        logger.debug(f"Sending message about {message.get('cls')}")
        self.queue.put(message)
