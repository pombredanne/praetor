import prefect
from prefect import schedules
from praetor import Flow, Task, task
import time
from random import randint
from datetime import timedelta


schedule = schedules.IntervalSchedule(interval=timedelta(minutes=1))
flow = Flow("large_example_flow")


def tsk(x=None):
    time.sleep(randint(3, 5))


with flow:
    start = task(tsk, name="start")

    syncs = [
        "sync__BOB5",
        "sync__BOB6",
        "sync__GRP",
        "sync__LYU1",
        "sync__LYU2",
        "sync__LYU3-4",
        "sync__RIK",
        "sync__ZHU",
    ]

    sync_map = task(tsk, name="sync")
    x = sync_map.map(syncs)
    start.set_downstream(x)

#     delete_tc = task(tsk, name="delete_tc")
#     copy_tc = task(tsk, name="copy_tc")
#     start.set_downstream(delete_tc)
#     delete_tc.set_downstream(copy_tc)

#     delete_sc = task(tsk, name="delete_sc")
#     swap_sc = task(tsk, name="swap_sc")
#     start.set_downstream(delete_sc)
#     sc = [
#         "copy__BOB5",
#         "copy__BOB6",
#         "copy__GRP",
#         "copy__LYU1",
#         "copy__LYU2",
#         "copy__LYU3-4",
#         "copy__RIK",
#         "copy__ZHU",
#     ]
#     for name in sc:
#         t = task(tsk, name=name)
#         delete_sc.set_downstream(t)
#         swap_sc.set_upstream(t)

#     truncate_w = task(tsk, name="truncate_w")
#     start.set_downstream(truncate_w)
#     swap_w = task(tsk, name="swap_w")
#     ws = [
#         "copy__15lFg4",
#         "copy__180Wg0",
#         "copy__1AHVaV",
#         "copy__1TqKtS",
#         "copy__1mpZXm",
#         "copy__1u3g4u",
#         "copy__1zG-VZ",
#     ]
#     for name in ws:
#         t = task(tsk, name=name)
#         truncate_w.set_downstream(t)
#         swap_w.set_upstream(t)

#     trunc_agg = task(tsk, name="trunc_agg")
#     copy_agg = task(tsk, name="copy_agg")
#     swap_agg = task(tsk, name="swap_agg")
#     trunc_agg.set_upstream(start)
#     trunc_agg.set_downstream(copy_agg)
#     copy_agg.set_downstream(swap_agg)


# tasks_names = [
#     "copy__gdoc.staging_warehouse_aggregate_costs",
#     "push_masters_info",
#     "swap__gdoc.warehouse_aggregate_costs",
#     "swap__schedules",
#     "swap__warehouse_in_out",
#     "truncate__gdoc.staging_warehouse_aggregate_costs",
# ]


if __name__ == "__main__":
    flow.run(executor=prefect.engine.executors.DaskExecutor("localhost:8786"))
