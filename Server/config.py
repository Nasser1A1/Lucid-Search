from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Template"
    PROJECT_VERSION: str = "1.0.0"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    TAVILY_API_KEY: str = ""
    GOOGLE_GEMNINI_API_KEY: str = ""