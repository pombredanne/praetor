import os
import pathlib
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, PlainTextResponse, Response
from starlette.staticfiles import StaticFiles

from praetor import schemas
from praetor.server import crud
from praetor.server.collector import process_message
from praetor.server.db import Session

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


app.mount(
    "/static/",
    StaticFiles(directory=pathlib.Path(__file__).parent.parent / "static"),
    name="static",
)


@app.get("/")
def get_index():
    return FileResponse(
        path=pathlib.Path(__file__).parent.parent / "static" / "index.html",
        media_type="text/html",
    )


@app.get("/api/flows/", response_model=List[schemas.Flow])
def get_flows(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_flows(db, offset=offset, limit=limit)


@app.delete("/api/flows/{flow_id:int}/")
def delete_flow(flow_id: int, db: Session = Depends(get_db)):
    return crud.delete_flow(db, flow_id)


@app.get("/api/flows/{flow_id:int}/", response_model=schemas.FlowDetail)
def get_flow(flow_id: int, flow_runs=10, db: Session = Depends(get_db)):
    return crud.get_flow(db, flow_id, flow_runs=flow_runs)


@app.post("/api/flows/", response_model=schemas.Flow)
def create_flow(flow: schemas.NaiveFlow, db: Session = Depends(get_db)):
    return crud.post_flow(db, flow)


@app.post("/api/flow_runs/", response_model=schemas.FlowRun)
def create_flow_run(flow_run: schemas.NaiveFlowRun, db: Session = Depends(get_db)):
    return crud.post_flow_run(db, flow_run)


@app.post("/api/task_runs/", response_model=schemas.TaskRun)
def create_task_run(task_run: schemas.NaiveTaskRun, db: Session = Depends(get_db)):
    return crud.post_task_run(db, task_run)


@app.get("/api/dask/")
def get_dask():
    return PlainTextResponse(os.environ.get("DASK_UI"))


@app.post("/api/message/")
def receive_message(message: schemas.Message, db: Session = Depends(get_db)):
    process_message(db, message.dict())
    return PlainTextResponse("OK")
