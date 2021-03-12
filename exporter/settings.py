from environs import Env

env = Env()
env.read_env()

# Override in .env for local development
LOG_LEVEL = env.str("LOG_LEVEL", 'INFO').upper()
LOG_QUERIES = env.bool("LOG_QUERIES", default=False)
SQL_SCHEMA = env.str("SQL_SCHEMA", default=None)

# git related configuration
GH_REPO = env.str("GH_REPO", default=None)
GH_TOKEN = env.str("GH_TOKEN", default=None)

# ssh related configuration
SSH_ADDRESS = env.str("SSH_ADDRESS", default=None)
SSH_PORT = env.str("SSH_PORT", default=None)
SSH_USER = env.str("SSH_USER", default=None)
SSH_PASS = env.str("SSH_PASS", default=None)
SSH_FOLDER = env.str("SSH_FOLDER", default=None)

ID = env.str("ID", 'default')
