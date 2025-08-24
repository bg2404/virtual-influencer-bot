# Virtual Influencer Bot

This project is a Python-based bot that automatically generates and posts content for a virtual social media influencer on X (formerly Twitter). It leverages Large Language Models (LLMs) like Google's Gemini and OpenAI's GPT to create unique content based on predefined personalities and content types. All generated posts are stored in a Supabase database to avoid repetition and maintain a history.

## Features

-   **AI-Powered Content Generation**: Utilizes various LLMs to generate creative and engaging tweets.
-   **Customizable Persona**: Easily define the influencer's personality (e.g., "The Enthusiastic Optimist," "The Knowledgeable Guide") and the type of content to generate (e.g., "Informative Snippets," "Expert Tips").
-   **Automated Posting**: Directly posts the generated content to an X account.
-   **History Tracking**: Saves every post to a Supabase database to prevent duplicate content.
-   **Flexible Configuration**: Configure API keys, model preferences, and posting behavior using environment variables and command-line arguments.
-   **Scheduled Execution**: Includes a GitHub Actions workflow to run the bot on a schedule (e.g., every 6 hours) or manually.

## Tech Stack

-   **Language**: Python 3.11+
-   **Dependency Management**: Poetry
-   **LLM APIs**: Google Gemini, OpenAI
-   **Social Media**: Tweepy for the X API v2
-   **Database**: Supabase
-   **CI/CD**: GitHub Actions

## Project Structure

```
.
├── .github/workflows/
│   └── post-content.yml    # GitHub Actions workflow for scheduled posting
├── data/
│   ├── content_format.json # Defines content formats (e.g., Text)
│   ├── content_type.json   # Defines content types (e.g., Informative Snippets)
│   └── personality_type.json # Defines influencer personalities
├── models/
│   ├── llm.py              # Pydantic models for LLM configurations
│   └── tweet.py            # Pydantic model for a Tweet record
├── utils/
│   ├── api_client.py       # Handles LLM API client initialization
│   ├── api_config.py       # Loads API credentials from environment
│   ├── db_handler.py       # Manages Supabase database interactions
│   ├── generate_prompt.py  # Constructs the prompt for the LLM
│   ├── load_json.py        # Helpers to load data files
│   └── post.py             # Handles posting to social media
├── .env.example            # Example environment variables file
├── main.py                 # Main application entry point
└── pyproject.toml          # Project dependencies and configuration
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/virtual-influencer-bot.git
    cd virtual-influencer-bot
    ```

2.  **Install Poetry** (if you haven't already):
    ```bash
    pip install poetry
    ```

3.  **Install dependencies:**
    ```bash
    poetry install
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory by copying the `.env.example` file. Then, fill in your credentials.
    ```bash
    cp .env.example .env
    ```
    You will need to populate it with your API keys and tokens from Google, OpenAI, X, and Supabase.

## Usage

You can run the bot directly from your command line.

```bash
poetry run python main.py [OPTIONS]
```

### Command-Line Arguments

-   `--model`: (Required) The LLM to use (e.g., `gemini-2.5-pro`, `gpt-4o`).
-   `--personality`: (Required) The personality for the tweet.
-   `--content-type`: (Required) The type of content for the tweet.
-   `--include-hashtags`: Flag to include hashtags.
-   `--include-emojis`: Flag to include emojis.
-   `--post`: Flag to post the generated tweet to X. If not set, the tweet is only printed to the console.

### Example

```bash
poetry run python main.py \
  --model "gemini-2.5-pro" \
  --personality "The Knowledgeable Guide" \
  --content-type "Informative Snippets and Facts" \
  --post
```

## Automation with GitHub Actions

The included `.github/workflows/post-content.yml` workflow allows for automated, scheduled content generation and posting.

-   **Triggers**: Runs every 6 hours (`cron: '0 */6 * * *'`) and can also be triggered manually from the Actions tab in your GitHub repository.
-   **Configuration**: To use the workflow, you must add the following as repository secrets in your GitHub project settings (`Settings > Secrets and variables > Actions`):
    -   `GEMINI_API_KEY`
    -   `GEMINI_BASE_URL`
    -   `OPENAI_API_KEY`
    -   `OPENAI_BASE_URL`
    -   `X_USERNAME`
    -   `X_API_KEY`
    -   `X_API_KEY_SECRET`
    -   `X_ACCESS_TOKEN`
    -   `X_ACCESS_TOKEN_SECRET`
    -   `SUPABASE_URL`
    -   `SUPABASE_KEY`
    -   `MODEL`
    -   `PERSONALITY`
    -   `CONTENT_TYPE`
    -   `INCLUDE_HASHTAGS` (e.g., `true`)
    -   `INCLUDE_EMOJIS` (e.g., `true`)
    -   `POST` (e.g., `true`)