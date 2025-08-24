from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Tweet(BaseModel):
    """
    Model for storing generated tweets.
    """

    id: Optional[int] = None
    model_name: str
    personality: str
    content_type: str
    content_format: str
    tweet_text: str
    posted_url: Optional[str] = None  # URL if posted successfully
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Tweet(tweet_text='{self.tweet_text[:50]}...', posted_url='{self.posted_url}')>"
