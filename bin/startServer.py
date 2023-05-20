#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from multiprocessing.context import SpawnProcess

from uvicorn import Server, Config
from uvicorn.supervisors import Multiprocess

from jukebox.scheduler import run_scheduler
from jukebox.utils import get_logger, logging_config

logger = get_logger()

run_config: dict = {
    'app': 'jukebox.main:app',
    'host': 'localhost',
    'port': 8000,
    'workers': 4,
    'log_config': logging_config,
}


class Application(Multiprocess):

    def __init__(self, **kwargs):
        config = Config(**kwargs)
        super().__init__(config, target=Server(config).run, sockets=[config.bind_socket()])

    def startup(self) -> None:
        super().startup()

        # Start scheduler process
        scheduler = SpawnProcess(target=run_scheduler)
        scheduler.start()
        self.processes.append(scheduler)


if __name__ == "__main__":
    logger.info("Starting development server at http://%s:%d/", run_config['host'], run_config['port'])
    logger.info("Quit the server with CONTROL-C.")

    Application(**run_config).run()
