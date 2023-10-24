import os

APP_ENV = os.getenv("APP_ENV", "dev")
VERSION = os.getenv("CI_COMMIT_TAG", "0.0.0")
