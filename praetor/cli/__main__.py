from praetor.cli.run import run
from praetor.cli.collector import Collector

import argparse
import uvicorn
import os
import re


url_re = re.compile(r"(tcp://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*")


def webserver(args):
    url = url_re.match(args.dask)
    if not url:
        raise ValueError(f"Couldn't parse URL: {args.dask}")
    host = url.group("host")
    dask_ui = f"http://{host}:{args.ui_port or 8787}"
    os.environ["DASK"] = args.dask
    os.environ["DASK_UI"] = dask_ui
    print(args.dask, url, dask_ui)
    collector = Collector(dask=args.dask)
    collector.start()
    uvicorn.run("praetor.cli.webserver:app", reload=True)
    collector.stop()
    collector.join()


def _run(args):
    run(args.location, address=args.dask)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="command")

webserver_parser = subparsers.add_parser("webserver")
webserver_parser.set_defaults(func=webserver)
webserver_parser.add_argument("--dask", action="store", default="tcp://127.0.0.1:8786")
webserver_parser.add_argument("--ui-port", action="store")

run_parser = subparsers.add_parser("run")
run_parser.add_argument("location")
run_parser.add_argument("--dask", action="store", default="tcp://127.0.0.1:8786")
run_parser.set_defaults(func=_run)

args = parser.parse_args()
args.func(args)
