import prefect
import time
from datetime import timedelta
from pprint import pprint


class Task1(prefect.Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        run = prefect.context["scheduled_start_time"].strftime("%Y-%m-%d %H:%M:%S")
        self.logger.warning(pprint(prefect.context.__dict__))
        return 5


@prefect.task
def task2(x):
    pass


schedule = prefect.schedules.CronSchedule("* * * * *")
flow = prefect.Flow("test_flow_name", schedule=schedule)

with flow:
    task2(Task1())


if __name__ == "__main__":
    flow.run()
