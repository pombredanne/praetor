# What it is

Praetor is a minimal Web UI for monitoring [Prefect Core](https://docs.prefect.io) flows. Airflow is so awesome because of it's UI and it's sad that even more awesome Prefect Core lacks one.

This is strictly for monitoring task states and looking at logs. If you need a fully managed solution, consider using [Prefect Cloud](https://prefect.io).

# What it does

There are two parts to Praetor: webserver and custom classes. Webserver lets you look at what's going on with your flows and runner is used to run flows. Custom classes are the same as normal Prefect classes: Flow, Task and `@task` decorator. The difference is that they report their state to the webserver.

I tried to improve on the parts of Airflow UI that I didn't like:

- It's realtime and updates itself, so no need to manually hit refresh every 5 seconds.
- In tree view (it's the only option for now) one task is displayed exactly once. Tasks are topologically sorted, so all displayed connections are top-down.

# What it doesn't

- Handle your flows for you (starting, restarts etc.)
- Manage your secrets
- Authenticate users

# Usage

To start webserver, run

```bash
$ praetor webserver --dask localhost:8786
```

`--dask` is optional. If you don't provide the dask option, the server will only be available in local mode.

To run a flow, do:

```py
from praetor import Flow, Task, task  # instead of: from prefect import Flow, Task, task
```

then proceed as usual.

These are subclasses of normal prefect classes, but with additional state handlers and hooks for reporting start/stop of the flow. If you use `DaskExecutor`, the flow will push update messages into a Queue on the dask cluster. If you're not using it, it will try and use a simple REST API at http://localhost:8000, which is called "local mode".

# Installation

For now, clone and run `$ python setup.py install -e '.[webserver]`. Note that this is not ready for production at all, so use at your own peril.

Note that both prefect and praetor need to be installed on Dask workers. See `examples` folder for an example Dockerfile and Compose setup.
