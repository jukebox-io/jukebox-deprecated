from starlette.config import Config

# The configuration will be read from different sources in the following order:
#   1. Environment Variables (mostly used during production)
#   2. development.conf (if available, sets development defaults for required configurations)
#   3. Default value (some of the configuration is optional and will be assigned default value automatically)

# read development config if present
settings = Config(env_file="misc/development.conf")
