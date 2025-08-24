from utils.api_config import GEMINI_API, OPENAI_API


class Model:
    """Represents an AI model with its configuration."""

    name: str  # User-friendly display name (e.g., "GPT-4o")
    model_name: str  # API identifier (e.g., "gpt-4o")
    api: dict  # Associated API configuration (GEMINI_API or OPENAI_API)

    def __init__(self, name, model_name, api):
        self.name = name
        self.model_name = model_name
        self.api = api

    def __repr__(self):
        return f"Model(name={self.name}, model_name={self.model_name})"

    def __str__(self):
        return self.name


GEMINI_2_5_PRO = Model(
    name="Gemini 2.5 Pro",
    model_name="gemini-2.5-pro",
    api=GEMINI_API,
)

GEMINI_2_5_FLASH = Model(
    name="Gemini 2.5 Flash",
    model_name="gemini-2.5-flash",
    api=GEMINI_API,
)

GEMINI_2_5_FLASH_LITE = Model(
    name="Gemini 2.5 Flash Lite",
    model_name="gemini-2.5-flash-lite",
    api=GEMINI_API,
)

O3 = Model(
    name="O3",
    model_name="o3-2025-04-16",
    api=OPENAI_API,
)

O4_MINI = Model(
    name="O4 Mini",
    model_name="o4-mini-2025-04-16",
    api=OPENAI_API,
)

GPT_4O = Model(
    name="GPT-4o",
    model_name="gpt-4o",
    api=OPENAI_API,
)

GPT_4O_MINI = Model(
    name="GPT-4o Mini",
    model_name="gpt-4o-mini",
    api=OPENAI_API,
)

MODEL_OPTIONS = {
    GEMINI_2_5_PRO.model_name: GEMINI_2_5_PRO,
    GEMINI_2_5_FLASH.model_name: GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE.model_name: GEMINI_2_5_FLASH_LITE,
    O3.model_name: O3,
    O4_MINI.model_name: O4_MINI,
    GPT_4O.model_name: GPT_4O,
    GPT_4O_MINI.model_name: GPT_4O_MINI,
}
