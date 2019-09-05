from praetor.tests.fixtures import flow_no_schedule, flow
from praetor import schemas

import pytest


class TestNaiveFlowSchema:
    def test_get_schedule_no_schedule_ok(self):
        try:
            schemas.NaiveFlow.get_schedule(None)
        except AttributeError:
            pytest.fail(
                "Unexpected AttributeError, get_schedule should accept None as schedule"
            )

    def test_schedule_extraction(self, flow):
        f = schemas.NaiveFlow.from_prefect(flow)
        assert f.schedule == "* * * * *"

    def test_task_index_present(self, flow):
        f = schemas.NaiveFlow.from_prefect(flow)
        for task in f.tasks:
            assert task.index is not None
