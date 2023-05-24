# LLM class
from typing import List
import openai

from models import ChatGPTMessage
openai_key = None


class LLM:
    def __init__(self):
        openai.api_key = openai_key

    # TODO move into agent to generate prompt!
    # TODO add choosing a model from config ect.
    def generate_response(self, messages: List[ChatGPTMessage]):
        # Placeholder implementation, replace with actual ChatGPT interaction
        # print([message.dict() for message in messages])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[message.dict() for message in messages],
        )
        return response["choices"][0]["message"]["content"]
        # return "test"
