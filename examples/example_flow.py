import prefect
import time
from datetime import timedelta


class Task1(prefect.Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        time.sleep(5)
        run = prefect.context["scheduled_start_time"].strftime("%Y-%m-%d %H:%M:%S")
        self.logger.warning(f"CURRENT RUN: {run}")
        return 5


@prefect.task
def task2(x):
    time.sleep(5)
    return x


@prefect.task(max_retries=3, retry_delay=timedelta(seconds=5))
def task3(x):
    time.sleep(5)
    if prefect.context.get("task_run_count") == 1:
        raise ValueError("fake error")
    return x


@prefect.task
def task4(x, y):
    time.sleep(5)
    return x


schedule = prefect.schedules.CronSchedule("* * * * *")
flow = prefect.Flow("example_flow", schedule=schedule)

with flow:
    x = Task1()
    task2(x)
    task4(x, task3(x))


if __name__ == "__main__":
    flow.run(executor=prefect.engine.executors.LocalDaskExecutor())
