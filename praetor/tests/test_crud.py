from praetor.tests.fixtures import flow_no_schedule, flow, db
from praetor import models
from praetor import schemas
from praetor import crud


def test_post_flow(db, flow):
    f = schemas.NaiveFlow.from_prefect(flow)
    res = crud.post_flow(db, f)

    assert isinstance(res, models.base.Base)
    assert db.query(models.Flow).count() == 1
    assert len(res.tasks) == len(flow.tasks)
    assert db.query(models.Task).filter_by(flow=res).count() == len(flow.tasks)
    assert len(res.edges) == len(flow.edges)
    assert db.query(models.Edge).filter_by(flow=res).count() == len(flow.edges)
    assert res.schedule is not None


def test_delete_flow(db, flow):
    f = schemas.NaiveFlow.from_prefect(flow)
    f.name = "flow_to_delete"
    flow = crud.post_flow(db, f)
    flow_id = flow.id
    flow.is_online = False
    db.commit()

    assert db.query(models.Flow).get(flow_id) is not None
    crud.delete_flow(db, flow_id)
    assert db.query(models.Flow).get(flow_id) is None


def test_delete_flow_not_working_if_online(db, flow):
    f = schemas.NaiveFlow.from_prefect(flow)
    f.name = "flow_not_to_delete"
    flow = crud.post_flow(db, f)
    flow.is_online = True
    db.commit()
    flow_id = flow.id

    assert db.query(models.Flow).get(flow_id) is not None
    crud.delete_flow(db, flow_id)
    assert db.query(models.Flow).get(flow_id) is not None


def test_post_flow_run(db, flow):
    f = schemas.NaiveFlow.from_prefect(flow)

    flow_run = schemas.NaiveFlowRun(key="2019-01-01 00:00:00", flow=f, state="Success")
    crud.post_flow_run(db, flow_run)

    flow_run = schemas.NaiveFlowRun(key="2019-01-01 00:01:00", flow=f, state="Running")
    crud.post_flow_run(db, flow_run)

    assert db.query(models.FlowRun).filter_by(state="Success").count() == 1
    assert db.query(models.FlowRun).filter_by(state="Running").count() == 1


def test_post_task_run(db, flow):
    f = schemas.NaiveFlow.from_prefect(flow)

    flow_run1 = schemas.NaiveFlowRun(key="2019-01-01 00:00:00", flow=f, state="Success")
    for task in f.tasks:
        t = schemas.NaiveTask.from_prefect(task)
        task_run = schemas.NaiveTaskRun(task=t, flow_run=flow_run1, state="Success")
        crud.post_task_run(db, task_run)

    flow_run2 = schemas.NaiveFlowRun(key="2019-01-01 00:01:00", flow=f, state="Running")
    for task in f.tasks:
        t = schemas.NaiveTask.from_prefect(task)
        task_run = schemas.NaiveTaskRun(task=t, flow_run=flow_run2, state="Running")
        crud.post_task_run(db, task_run)

    assert db.query(models.TaskRun).filter_by(state="Success").count() == len(f.tasks)
    assert db.query(models.TaskRun).filter_by(state="Running").count() == len(f.tasks)
