import logging

from openai import APIError, APITimeoutError, OpenAI

logger = logging.getLogger(__name__)


def get_api_client(api_config: dict):
    """
    Initializes and returns an API client based on the provided configuration.
    Manages client instances in Streamlit's session state.

    Args:
        api_config (dict): Dictionary containing API details ('key', 'base_url', 'name').

    Returns:
        An initialized API client instance (e.g., openai.OpenAI) or None if initialization fails.
    """
    api_key = api_config.get("key")
    base_url = api_config.get("base_url")
    api_name = api_config.get("name", "UnknownAPI")
    client = None
    try:
        if "OpenAI" in api_name:
            effective_base_url = base_url if base_url else None
            client = OpenAI(api_key=api_key, base_url=effective_base_url)

        elif "Gemini" in api_name:
            effective_base_url = base_url if base_url else None
            if not effective_base_url:
                logger.error(f"Base URL is required for {api_name} but not found in config.")
                raise ValueError("Base URL is required for Gemini but not found.")
            # Attempting to use OpenAI client library for Google models. Ensure endpoint is compatible.
            client = OpenAI(api_key=api_key, base_url=effective_base_url)

        else:
            logger.error(f"Client initialization not defined for API type: {api_name}")
            raise ValueError(f"Client initialization not defined for API type: {api_name}")

        return client

    except APITimeoutError as e:
        logger.error(f"API Timeout during client initialization for {api_name}: {e}")
        raise e
    except APIError as e:
        logger.error(f"API Error during client initialization for {api_name}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to initialize API client for {api_name}: {e}")
        raise e
