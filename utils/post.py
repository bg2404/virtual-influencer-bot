from utils.api_config import X_API


class SocialMediaPoster:
    def __init__(self, platform, api_config):
        self.platform = platform
        self.api_config = api_config
        self.client = self.initialize_client()

    def initialize_client(self):
        if self.platform == "X":
            import tweepy

            return tweepy.Client(
                consumer_key=self.api_config.get("api_key"),
                consumer_secret=self.api_config.get("api_key_secret"),
                access_token=self.api_config.get("access_token"),
                access_token_secret=self.api_config.get("access_token_secret"),
            )
        raise NotImplementedError(f"Platform {self.platform} is not supported.")

    def post(self, content):
        if self.platform == "X":
            try:
                if X_API.get("username") is None:
                    raise ValueError("X API username is not configured.")
                response = self.client.create_tweet(text=content)
                return f"https://x.com/{self.api_config.get('username')}/status/{response.data['id']}"
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise e
        raise NotImplementedError(f"Posting to {self.platform} is not implemented.")
