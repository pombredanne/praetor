# What it is

Praetor is a minimal Web UI for monitoring [Prefect Core](https://docs.prefect.io) flows. Airflow is so awesome because of it's UI and it's sad that even more awesome Prefect Core lacks one.

This is strictly for monitoring task states and looking at logs. If you need a fully managed solution, consider using [Prefect Cloud](https://prefect.io).

# What it does

There are two parts to Praetor: webserver and flow runner. Webserver lets you look at what's going on with your flows and runner is used to run flows. Runner injects all the necessary state handlers to your flows and tasks and makes the report their state to webserver.

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
$ praetor webserver --dask tcp://localhost:8786
```

`--dask` is optional, the default is `tcp://127.0.0.1:8786`. Then go to [localhost:8000](http://localhost:8000/) to see your Web UI.

To run a flow, do:

```bash
$ praetor run your_flow.py --dask tcp://localhost:8786
```

You can use your flow files as-is, with two important requirements:

- Your flow needs to be importable from the file as `flow`.
- You should "hide" your default `flow.run()` call, the runner will call it for you:
  ```py
  if __name__ == "__main__":
      flow.run()
  ```

Dask uses `dask.distributed.Queue` for communication between webserver and runners, so dask cluster is required.

# Installation

For now, clone and run `$ python setup.py install -e '.[webserver]`. Note that this is not ready for production at all, so use at your own peril.

# What needs to be done, but isn't

- Configuration with config file, env variables and cli options. For example, right now sqlalchemy connection is hardcoded as `postgresql://praetor:praetor@localhost/praetor`.
- More tests.
- CI
- PyPi
- Make basic usage not require a running dask cluster. Runners and webserver should check if there's a LocalCluster at the default address and use that or create one.
- Refactoring UI components on frontend. I'm not quite happy with how it's organized right now.
- Send logs from workers and flow.
- Generate readable notifications for important events (like retries and failed states).
- Write documentation.
