#  Copyright 2023 by JukeBox Developers. All rights reserved.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

from jukebox.settings import settings
from jukebox.utils import NUM_CORES

# -------------------------------------------------------
# Deployment
# -------------------------------------------------------
# Server deployment is a complex area, that will depend on what kind of service you're deploying
# Uvicorn onto. As a general rule, you probably want to:
#   - Run uvicorn --reload from the command line for local development.
#   - Run gunicorn -k uvicorn.workers.UvicornWorker for production.
#   - Additionally run behind Nginx for self-hosted deployments.
#   - Finally, run everything behind a CDN for caching support, and serious DDOS protection.
# Refer to, https://www.uvicorn.org/deployment/

# Server Mechanics
preload_app = True

# Worker Configuration
worker_class = "uvicorn.workers.UvicornWorker"

workers: int = settings.get("WEB_CONCURRENCY", cast=int, default=None)
if not workers:
    # Gunicorn relies on the operating system to provide all the load balancing when handling
    # requests. Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off
    # with. While not overly scientific, the formula is based on the assumption that for a given
    # core, one worker will be reading or writing from the socket while the other worker is
    # processing a request.
    # Refer to, https://docs.gunicorn.org/en/stable/design.html#how-many-workers

    workers = 2 * NUM_CORES + 1

# Logging Configuration
accesslog = "-"  # log requests to stdout
