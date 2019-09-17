import time
from datetime import timedelta

import prefect

from praetor import Flow, Task, task


class Task1(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        time.sleep(5)
        run = prefect.context["scheduled_start_time"].strftime("%Y-%m-%d %H:%M:%S")
        self.logger.warning(f"CURRENT RUN: {run}")
        return list(range(5))


@task
def task2(x):
    time.sleep(x)
    return x


@task(max_retries=3, retry_delay=timedelta(seconds=5))
def task3(x):
    time.sleep(5)
    if prefect.context.get("task_run_count") == 1:
        raise ValueError("fake error")
    return x


@task
def task4(xs, y):
    time.sleep(5)
    return x


schedule = prefect.schedules.CronSchedule("* * * * *")
flow = Flow("example_flow")

with flow:
    x = Task1()
    xs = task2.map(x)
    task4(xs, task3(x))


if __name__ == "__main__":
    flow.run(executor=prefect.engine.executors.DaskExecutor(address="127.0.0.1:8786"))
