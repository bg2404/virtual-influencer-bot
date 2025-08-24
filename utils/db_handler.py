from supabase import Client, create_client

from models.tweet import Tweet

from .api_config import SUPABASE_API


class DatabaseHandler:
    """
    Handles database interactions for storing generated tweets.
    """

    client: Client
    table_name: str

    def __init__(self):
        """Initializes the database connection."""
        self.client: Client = create_client(SUPABASE_API["url"], SUPABASE_API["key"])
        self.table_name: str = "tweets"

    def add_tweet(self, model_name, personality, content_type, content_format, tweet_text, posted_url=None):
        """
        Adds a tweet to the database.

        Args:
            model_name (str): The name of the model used to generate the tweet.
            personality (str): The personality used for tweet generation.
            content_type (str): The content type of the tweet.
            content_format (str): The format of the tweet.
            tweet_text (str): The generated tweet text.
            posted_url (str, optional): The URL where the tweet was posted. Defaults to None.
        """
        try:
            new_tweet = Tweet(
                model_name=model_name,
                personality=personality,
                content_type=content_type,
                content_format=content_format,
                tweet_text=tweet_text,
                posted_url=posted_url,
            )
            tweet_data = new_tweet.model_dump(exclude={"id", "created_at"}, exclude_none=True)
            print(f"Adding tweet to database: {tweet_data}")

            response = self.client.table(self.table_name).insert(tweet_data).execute()

            if response.data:
                inserted_tweet_id = response.data[0]["id"]
                print(f"Tweet saved to database with id {inserted_tweet_id}")
                return inserted_tweet_id
            else:
                print(
                    f"Error adding tweet to database: {response.error.message if response.error else 'No data returned'}"
                )
                return None
        except Exception as e:
            print(f"Error adding tweet to database: {e}")
            return None

    def update_tweet_url(self, tweet_id, posted_url):
        """
        Updates the posted URL for a tweet in the database.

        Args:
            tweet_id (int): The ID of the tweet to update.
            posted_url (str): The URL where the tweet was posted.
        """
        try:
            response = (
                self.client.table(self.table_name).update({"posted_url": posted_url}).eq("id", tweet_id).execute()
            )
            if response.data:
                print(f"Tweet {tweet_id} updated with posted_url {posted_url}")
            else:
                print(
                    f"Tweet with id {tweet_id} not found or error updating: {response.error.message if response.error else 'Update failed'}"
                )
        except Exception as e:
            print(f"Error updating tweet: {e}")

    def get_all_tweets(self):
        """
        Retrieves all tweets from the database.

        Returns:
            list: A list of all tweets.
        """
        try:
            response = self.client.table(self.table_name).select("*").order("created_at", desc=True).execute()
            if response.data:
                return [Tweet(**tweet_data) for tweet_data in response.data]
            return []
        except Exception as e:
            print(f"Error getting all tweets: {e}")
            return []

    def get_tweet(self, tweet_id):
        """
        Retrieves a tweet from the database by ID.

        Args:
            tweet_id (int): The ID of the tweet to retrieve.

        Returns:
            Tweet: The tweet object, or None if not found.
        """
        try:
            response = self.client.table(self.table_name).select("*").eq("id", tweet_id).single().execute()
            if response.data:
                return Tweet(**response.data)
            return None
        except Exception as e:
            print(f"Error getting tweet {tweet_id}: {e}")
            return None


# Example Usage (for testing)
if __name__ == "__main__":
    db_handler = DatabaseHandler()  # Uses SQLite by default
    # Add a tweet
    tweet_id = db_handler.add_tweet(
        model_name="GPT-4o",
        personality="Enthusiastic Optimist",
        content_type="Informative Snippets and Facts",
        content_format="Text",
        tweet_text="This is a test tweet!",
    )

    if tweet_id:
        # Update the tweet with a posted URL
        db_handler.update_tweet_url(tweet_id, "https://x.com/example/status/12345")

        # Retrieve the tweet
        retrieved_tweet = db_handler.get_tweet(tweet_id)
        print(f"Retrieved tweet: {retrieved_tweet}")
