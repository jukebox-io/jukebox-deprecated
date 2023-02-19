from jukebox.core.settings import DEFAULT_PORT, GUNICORN_WORKERS_COUNT

# Configure Production Server

# Server deployment is a complex area, that will depend on what kind of service you're deploying
# onto. As a general rule, you probably want to:
#   - Run uvicorn --reload from the command line for local development.
#   - Run gunicorn -k uvicorn.workers.UvicornWorker for production.
#   - Additionally run behind Nginx for self-hosted deployments.
#   - Finally, run everything behind a CDN for caching support, and serious DDOS protection.

# Refer to, https://www.uvicorn.org/deployment/


# Server socket
bind = '%s:%s' % ('0.0.0.0', DEFAULT_PORT)  # serve on public ip address

# Worker processes
workers = GUNICORN_WORKERS_COUNT
worker_class = 'uvicorn.workers.UvicornWorker'

# Server mechanics
preload_app = True

# Logging
accesslog = '-'  # log requests to stdout
