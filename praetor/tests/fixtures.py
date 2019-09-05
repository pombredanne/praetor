from praetor.models.base import Base
import pytest
import prefect

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@pytest.fixture
def flow_no_schedule():
    @prefect.task
    def task1():
        return 5

    @prefect.task
    def task2(x):
        return x

    @prefect.task
    def task3(x):
        return x

    @prefect.task
    def task4(x):
        return x

    flow = prefect.Flow("test_flow_name")
    with flow:
        x = task1()
        task2(x)
        task4(task3(x))
        return flow


@pytest.fixture
def flow(flow_no_schedule):
    flow_no_schedule.schedule = prefect.schedules.CronSchedule("* * * * *")
    return flow_no_schedule


@pytest.fixture(scope="module")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
