#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import uvicorn

from jukebox.utils import get_logger, logging_config

logger = get_logger()

run_config: dict = {
    'app': 'jukebox.main:app',
    'host': 'localhost',
    'port': 8000,
    'workers': 5,
    'log_config': logging_config,
}

if __name__ == "__main__":
    logger.info("Starting development server at http://%s:%d/", run_config['host'], run_config['port'])
    logger.info("Quit the server with CONTROL-C.")
    uvicorn.run(**run_config)
