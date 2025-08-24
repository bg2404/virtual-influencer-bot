from utils.db_handler import DatabaseHandler


def generate_prompt(personality, content_type, content_format, include_hashtags=True, include_emojis=True):
    """
    Generates a prompt for the LLM to create a tweet, emphasizing variety and clarity.

    Args:
        personality (str): The influencer's personality (e.g., witty, energetic).
        content_type (str): The tweet's topic (e.g., news, entertainment).
        content_format (str): The desired style (e.g., informative, humorous).
        include_hashtags (bool): Whether to include hashtags.
        include_emojis (bool): Whether to include emojis.

    Returns:
        str: The generated prompt.
    """

    prompt = """
    **Persona:** You are a virtual social media influencer on X.com with a {personality} personality.

    **Objective:** Generate a single, engaging tweet (maximum 280 characters) that is:

    * Original and provides value to the audience (informative, entertaining, or engaging).
    * Concise, clear, and written in a natural, human-like style (avoid robotic phrasing).
    * Compliant with X.com's content policies (avoid spam or harmful content).

    **Content:** The tweet should be about {content_type} and formatted as {content_format}.

    **Instructions:**

    1.  Write ONLY the tweet text. Do not include a title, introduction, or signature.
    2.  Use a conversational tone, as if speaking directly to your followers.
    3.  {hashtag_instructions}
    4.  {emoji_instructions}
    5.  Do not generate tweets that are similar to the previous tweets.

    **Previous Tweets (Do NOT repeat or directly reference these):**
    {previous_tweets}

    **Example:**
    (Provide 1-2 examples of good tweets here, tailored to the personality and content type)

    **Your Tweet:**
    """.strip()  # Remove leading/trailing whitespace

    hashtag_instructions = (
        "Include 1-3 relevant hashtags to increase visibility." if include_hashtags else "Do not include any hashtags."
    )
    emoji_instructions = (
        "Use emojis to enhance engagement and express your personality." if include_emojis else "Do not use emojis."
    )

    # Get previous tweets from the database
    db_handler = DatabaseHandler()
    previous_tweets = db_handler.get_all_tweets()
    previous_tweets_text = "\n".join(f"- {tweet.tweet_text}" for tweet in previous_tweets)
    if not previous_tweets_text:
        previous_tweets_text = "None"

    prompt = prompt.format(
        personality=personality,
        content_type=content_type,
        content_format=content_format,
        hashtag_instructions=hashtag_instructions,
        emoji_instructions=emoji_instructions,
        previous_tweets=previous_tweets_text,
    )
    return prompt
