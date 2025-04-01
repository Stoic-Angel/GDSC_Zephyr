from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_NAME = "GDSC Zephyr"
    PROJECT_VERSION = "[ALPHA]"

    DB_URL = os.getenv("DB_URL")

    JWT_ACCESS_KEY = os.getenv("JWT_ACCESS_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    SESSION_EXPIRY = int(os.getenv("SESSION_EXPIRY"))
    CHARACTER_LIMIT = int(os.getenv("CHARACTER_LIMIT", 250))

    SECRET_KEY = os.getenv("SECRET_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
