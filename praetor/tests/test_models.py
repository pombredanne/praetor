from praetor.tests.fixtures import db, flow, flow_no_schedule
from praetor import schemas, models, crud


def test_flow_shutdown(db, flow):  # TODO: wrap into test class
    f = schemas.NaiveFlow.from_prefect(flow)
    f.name = "flow_to_shutdown"
    db_flow = crud.post_flow(db, f)

    flow_run1 = schemas.NaiveFlowRun(key="2019-01-01 00:00:00", flow=f, state="Success")
    crud.post_flow_run(db, flow_run1)
    for task in f.tasks:
        t = schemas.NaiveTask.from_prefect(task)
        task_run = schemas.NaiveTaskRun(task=t, flow_run=flow_run1, state="Success")
        crud.post_task_run(db, task_run)

    flow_run2 = schemas.NaiveFlowRun(key="2019-01-01 00:01:00", flow=f, state="Running")
    crud.post_flow_run(db, flow_run2)
    for task in f.tasks:
        t = schemas.NaiveTask.from_prefect(task)
        task_run = schemas.NaiveTaskRun(task=t, flow_run=flow_run2, state="Running")
        crud.post_task_run(db, task_run)

    db_flow.shutdown()
    db.commit()

    assert (
        db.query(models.FlowRun)
        .filter(models.FlowRun.state.notin_(["Success", "Failed", "Canceled"]))
        .count()
        == 0
    )
    assert (
        db.query(models.TaskRun)
        .filter(models.TaskRun.state.notin_(["Success", "Failed", "Canceled"]))
        .count()
        == 0
    )
