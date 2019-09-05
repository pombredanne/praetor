from praetor.db import Session
from praetor import schemas
from praetor.models import Flow


def get_flows(db: Session, offset: int = 0, limit: int = 10):
    return db.query(Flow).offset(offset).limit(limit).all()


def post_flow(db: Session, flow: schemas.NaiveFlow):
    f = Flow.ensure(db, flow.name, is_online=flow.is_online, schedule=flow.schedule)
    if not flow.is_online:
        f.shutdown()
    else:
        f.create_session(db, tasks=flow.tasks, edges=flow.edges)
    db.commit()
    return f


def get_flow(db: Session, flow_id: int):
    return db.query(Flow).get(flow_id)


def delete_flow(db: Session, flow_id: int):
    flow = db.query(Flow).get(flow_id)
    if not flow.is_online:
        db.delete(flow)
        db.commit()
    return get_flows(db)


def post_flow_run(db: Session, flow_run: schemas.NaiveFlowRun):
    flow = Flow.ensure(db, flow_run.flow.name)
    flow_run = flow.latest_session.ensure_flow_run(
        db, flow_run.key, state=flow_run.state
    )
    db.commit()
    return flow_run


def post_task_run(db: Session, task_run: schemas.NaiveTaskRun):
    flow = Flow.ensure(db, task_run.flow_run.flow.name)
    task = flow.latest_session.ensure_task(db, task_run.task.name)
    flow_run = flow.latest_session.ensure_flow_run(db, task_run.flow_run.key)
    task_run = flow_run.ensure_task_run(db, task, state=task_run.state)
    db.commit()
    return task_run