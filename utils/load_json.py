import json


def load_json(filepath):
    """
    Load JSON data from a file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filepath}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def load_personalities(filepath="data/personality_type.json"):
    """
    Load personalities from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing personalities.

    Returns:
        dict: Dictionary of personalities.
    """
    return load_json(filepath)


def load_content_types(filepath="data/content_type.json"):
    """
    Load models from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing models.

    Returns:
        dict: Dictionary of models.
    """
    return load_json(filepath)


def load_content_formats(filepath="data/content_format.json"):
    """
    Load content formats from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing content formats.

    Returns:
        dict: Dictionary of content formats.
    """
    return load_json(filepath)
