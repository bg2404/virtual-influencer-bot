import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv

    from models.llm import MODEL_OPTIONS
    from utils.api_client import get_api_client
    from utils.api_config import X_API
    from utils.db_handler import DatabaseHandler
    from utils.generate_prompt import generate_prompt
    from utils.load_json import load_content_types, load_personalities
    from utils.post import SocialMediaPoster
except ImportError as e:
    logger.error("Failed to import a required module. Ensure all dependencies are installed.")
    logger.error(f"Details: {e}")
    raise e

# Load environment variables from a .env file if it exists
load_dotenv()


def generate_tweet_content(client, model, personality, content_type, include_hashtags, include_emojis):
    """Generates tweet content using the specified AI model and parameters."""
    prompt = generate_prompt(
        personality=personality,
        content_type=content_type,
        content_format="Text",  # Hardcoded for tweets
        include_hashtags=include_hashtags,
        include_emojis=include_emojis,
    )

    logger.info("Generating tweet content...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"❌ Error calling language model API: {e}")
        raise e


def post_and_save_tweet(tweet_content, model_name, personality, content_type):
    """Posts the tweet to X and saves it to the database."""
    logger.info("Posting tweet to X...")
    try:
        poster = SocialMediaPoster("X", api_config=X_API)
        status_url = poster.post(tweet_content)

        if not status_url:
            logger.error("❌ Failed to post tweet. The API may have returned an error.")
            raise ValueError("Failed to post tweet.")

        logger.info(f"✅ Tweet successfully posted! View it here: {status_url}")

        logger.info("Saving tweet to database...")
        db_handler = DatabaseHandler()
        db_handler.add_tweet(
            model_name=model_name,
            personality=personality,
            content_type=content_type,
            content_format="Text",
            tweet_text=tweet_content,
            posted_url=status_url,
        )
        logger.info("✅ Tweet saved to database.")

    except Exception as e:
        logger.error(f"❌ An error occurred during posting or saving: {e}")
        raise e


def main():
    """Main function to parse arguments and run the tweet generation process."""
    # Load dynamic choices for argparse
    try:
        personalities = list(load_personalities().keys())
        content_types = list(load_content_types().keys())
        model_names = list(MODEL_OPTIONS.keys())
    except FileNotFoundError as e:
        logger.error(f"Error: Could not load configuration JSON file. {e}")
        raise e

    parser = argparse.ArgumentParser(description="Generate and post a tweet from the command line.")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        choices=model_names,
        help="The model to use for generation.",
    )
    parser.add_argument(
        "--personality",
        type=str,
        required=True,
        choices=personalities,
        help="The personality for the tweet.",
    )
    parser.add_argument(
        "--content-type",
        type=str,
        required=True,
        choices=content_types,
        help="The type of content for the tweet.",
    )
    parser.add_argument(
        "--no-hashtags",
        action="store_false",
        dest="include_hashtags",
        help="Disable hashtags in the tweet.",
    )
    parser.add_argument(
        "--no-emojis",
        action="store_false",
        dest="include_emojis",
        help="Disable emojis in the tweet.",
    )
    parser.add_argument(
        "--post",
        action="store_true",
        help="Post the generated tweet to X. If not set, prints to console only.",
    )
    parser.set_defaults(include_hashtags=True, include_emojis=True)
    args = parser.parse_args()

    # Get API configuration for the selected model
    api_config = MODEL_OPTIONS.get(args.model).api
    if not api_config:
        logger.error(f"Error: No API configuration found for model '{args.model}'.")
        raise ValueError("No API configuration found.")

    # Initialize the API client
    client = get_api_client(api_config)
    if not client:
        logger.error(f"Error: Failed to initialize API client for {api_config.get('name')}.")
        logger.error("Please ensure the required API key environment variable is set.")
        raise ValueError("Failed to initialize API client.")

    # Generate Tweet
    tweet_text = generate_tweet_content(
        client,
        args.model,
        args.personality,
        args.content_type,
        args.include_hashtags,
        args.include_emojis,
    )

    if not tweet_text:
        logger.error("Stopping process due to content generation failure.")
        raise ValueError("Content generation failed.")

    print("\n--- Generated Tweet ---")
    print(tweet_text)
    print("-----------------------\n")

    # Post and/or save the tweet
    if args.post:
        post_and_save_tweet(
            tweet_text,
            args.model,
            args.personality,
            args.content_type,
        )
    else:
        print("Run with the --post flag to publish this tweet.")


if __name__ == "__main__":
    main()
