import os

from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API = {
    "name": "Gemini",
    "key": os.getenv("GEMINI_API_KEY"),
    "url": os.getenv("GEMINI_API_URL", "https://aistudio.google.com/app/apikey"),
    "base_url": os.getenv("GEMINI_BASE_URL"),
}

OPENAI_API = {
    "name": "OpenAI",
    "key": os.getenv("OPENAI_API_KEY"),
    "url": os.getenv("OPENAI_API_URL", "https://platform.openai.com/api-keys"),
    "base_url": os.getenv("OPENAI_BASE_URL"),
}

X_API = {
    "name": "X",
    "username": os.getenv("X_USERNAME"),
    "api_key": os.getenv("X_API_KEY"),
    "api_key_secret": os.getenv("X_API_KEY_SECRET"),
    "access_token": os.getenv("X_ACCESS_TOKEN"),
    "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET"),
    "client_id": os.getenv("X_CLIENT_ID"),
    "client_secret": os.getenv("X_CLIENT_SECRET"),
}

SUPABASE_API = {
    "name": "Supabase",
    "url": os.getenv("SUPABASE_URL"),
    "key": os.getenv("SUPABASE_KEY"),
}
