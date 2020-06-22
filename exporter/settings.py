from environs import Env

env = Env()
env.read_env()

# Override in .env for local development
LOG_LEVEL = env.str("LOG_LEVEL", 'INFO').upper()

GH_REPO = env.str("GH_REPO", default=None)
GH_TOKEN = env.str("GH_TOKEN", default=None)