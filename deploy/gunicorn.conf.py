from jukebox.settings import HOST, PORT, WEB_CONCURRENCY

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


# Server Bindings
bind = "%s:%s" % (HOST, PORT)

# Server Mechanics
preload_app = True

# Worker Configuration
workers = WEB_CONCURRENCY or 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logging Configuration
accesslog = "-"  # log requests to stdout
