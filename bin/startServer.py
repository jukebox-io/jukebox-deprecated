#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from uvicorn import Server, Config
from uvicorn.supervisors import Multiprocess

from jukebox.utils import get_logger, logging_config

logger = get_logger()

config = Config(
    app='jukebox.main:app',
    host='localhost',
    port=8000,
    workers=5,
    log_config=logging_config,
)


class Application(Server):
    pass


if __name__ == "__main__":
    logger.info("Starting development server at http://%s:%d/", config.host, config.port)
    logger.info("Quit the server with CONTROL-C.")

    # Configure
    application = Application(config)
    socket = config.bind_socket()
    supervisor = Multiprocess(config, target=application.run, sockets=[socket])

    # Run Server
    supervisor.run()
