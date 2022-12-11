import multiprocessing

from pxm.settings import PORT

# Configure Production Server (Gunicorn with Uvicorn Workers)

# Server deployment is a complex area, that will depend on what kind of service you're deploying
# onto.

# As a general rule, you probably want to:
#   - Run uvicorn --reload from the command line for local development.
#   - Run gunicorn -k uvicorn.workers.UvicornWorker for production.
#   - Additionally run behind Nginx for self-hosted deployments.
#   - Finally, run everything behind a CDN for caching support, and serious DDOS protection.

# Refer to, https://www.uvicorn.org/deployment/


# Server socket
bind = '%s:%s' % ('0.0.0.0', PORT)  # serve on public ip address

# Worker processes

# Gunicorn relies on the operating system to provide all the load balancing when handling
# requests. Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off
# with. While not overly scientific, the formula is based on the assumption that for a given
# core, one worker will be reading or writing from the socket while the other worker is
# processing a request.

# Refer to, https://docs.gunicorn.org/en/stable/design.html#how-many-workers

workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Server mechanics
wsgi_app = 'pxm.server:router'
preload_app = True

# Logging
accesslog = '-'
