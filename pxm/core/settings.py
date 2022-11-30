from starlette.config import Config

# Config will be read from environment variables and/or ".env" files.
server_config = Config('.env')
