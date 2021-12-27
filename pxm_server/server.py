import os
import platform
import sys
import time

import psutil


def start_server():
    # print default intro
    print_intro()

    if is_unix():
        # start unix server
        from .unix_server import start_unix_server
        start_unix_server()
    else:
        # start non-unix server
        from .non_unix_server import start_non_unix_server
        start_non_unix_server()


# // ---------------------------------------------------------------------------------------- utility fns

def print_intro() -> None:
    print(r"""
      _____         _      _    ____ ___
     |  ___|_ _ ___| |_   / \  |  _ \_ _|
     | |_ / _` / __| __| / _ \ | |_) | |
     |  _| (_| \__ \ |_ / ___ \|  __/| |
     |_|  \__,_|___/\__/_/   \_\_|  |___|

    ---- Powered By Gunicorn & Uvicorn ----
    """)

    # Debug Platform Info
    _cpu_freq = psutil.cpu_freq().max or psutil.cpu_freq().current

    print('Computer                     :', platform.node())
    print('System                       :', platform.platform())
    print()
    print('Python Version               :', platform.python_version())
    print('Python Native Compiler       :', platform.python_compiler())
    print('Python Build Info            :', *platform.python_build())
    print('Python Interpreter Info      :', *platform.architecture())
    print()
    print('System/OS Name               :', platform.system())
    print('System Release               :', platform.release())
    print('System Release Version       :', platform.version())
    print('Machine Type                 :', platform.machine())
    print('Processor Name               :', platform.processor() or 'Unknown')
    print('CPU core Count               :', 'Physical:', psutil.cpu_count(logical=False), '     Logical:',
          psutil.cpu_count(logical=True))
    print('CPU Frequency                :', round(_cpu_freq / 1000, 2), 'GHz, ', round(_cpu_freq), 'MHz')
    print('Total Physical Memory        :', _sizeof_fmt(psutil.virtual_memory().total))
    print()
    print('Host Address                 :', SERVER_HOST)
    print('Port Address                 :', SERVER_PORT)
    print('Worker Count                 :', SERVER_WORKER_COUNT)
    if is_unix(): print('Worker Class                 :', SERVER_WORKER_CLASS)
    print()
    print('Server Home                  :', os.getenv('pxm.home'))
    print()
    print()
    print('Starting FastAPI server ...')
    print()
    sys.stderr.flush()
    sys.stdout.flush()
    time.sleep(2)


def _sizeof_fmt(num: float, suffix: str = "B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def auto_detect_worker_count() -> int:
    """Returns an optimum number of workers w.r.t., system configuration of the server."""
    if is_unix():
        return max(psutil.cpu_count(logical=False) * 2 + 1, 2)
    else:
        return 1  # Uvicorn has problem with multiple worker


def is_unix() -> bool:
    try:
        import gunicorn.app.base
        return True
    except ImportError:
        # Can not load gunicorn
        return False


# // ---------------------------------------------------------------------------------------- server configurations

# DO NOT CHANGE THESE VALUES AT RUNTIME

SERVER_HOST = os.getenv('server.host') or '0.0.0.0'
SERVER_PORT = os.getenv('server.port') or 8080
SERVER_ROUTER = os.getenv('server.router')
SERVER_WORKER_COUNT = os.getenv('server.worker.count') or auto_detect_worker_count()
SERVER_WORKER_CLASS = os.getenv('server.worker.class')
