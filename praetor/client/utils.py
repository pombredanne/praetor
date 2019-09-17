from prefect import context as ctx


def get_run_key():
    return ctx.scheduled_start_time.strftime("%Y-%m-%d %H:%M:%S")


def get_flow():
    return ctx.flow
