import os

import openai
from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    """Create an OpenAI client using OPENAI_API_KEY from environment."""
    return openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
