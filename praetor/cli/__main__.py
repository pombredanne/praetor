from praetor.cli.run import run
from praetor.cli.collector import DaskPraetorCollector

import argparse
import uvicorn
import os
import re
import logging


logging.basicConfig(level="DEBUG")


def webserver(args):
    if args.dask is not None:
        collector = DaskPraetorCollector(address=args.dask)
        collector.start()
    uvicorn.run("praetor.cli.webserver:app", reload=True)
    if args.dask is not None:
        collector.stop()
        collector.join()


def _run(args):
    run(args.location, address=args.dask)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="command")

webserver_parser = subparsers.add_parser("webserver")
webserver_parser.set_defaults(func=webserver)
webserver_parser.add_argument("--dask", action="store")
webserver_parser.add_argument("--ui-port", action="store")

run_parser = subparsers.add_parser("run")
run_parser.add_argument("location")
run_parser.add_argument("--dask", action="store", default="tcp://127.0.0.1:8786")
run_parser.set_defaults(func=_run)

args = parser.parse_args()
args.func(args)
