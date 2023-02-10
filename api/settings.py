from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:54321/postgres"
)

PORT = env.str(
    "APP_PORT",
    default=5000
)

config = {
    'app_port': PORT,
    'database_url': DATABASE_URL
}

