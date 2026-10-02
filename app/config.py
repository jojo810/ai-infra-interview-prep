import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    open_api_key: str = os.getenv("OPENAI_API_KEY", "")
    open_ai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6")

settings = Settings()