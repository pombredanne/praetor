import signal


def register_shutdown_signals(shutdown_func):
    signal.signal(signal.SIGTERM, shutdown_func)
    signal.signal(signal.SIGINT, shutdown_func)
