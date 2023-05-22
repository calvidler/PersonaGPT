from typing import Union
from pydantic import BaseModel

from models import Agent


class Message(BaseModel):
    sender: Union[Agent, str]
    message: str
    timestamp: str

    def __init__(self, **args):
        super().__init__(**args)


class Conversation:
    messages: list[Message] = []

    def add_message(self, message: Message):
        print(message)
        self.messages.append(message)

    def to_string(self, skip_messages=0):
        prompt = ""
        sorted_messages = sorted(self.messages, key=lambda x: x.timestamp)

        # Skip messages from the start if skip_messages > 0
        messages_to_skip = min(skip_messages, len(sorted_messages))
        sorted_messages = sorted_messages[messages_to_skip:]

        for message in sorted_messages:
            if type(message.sender) == Agent:
                prompt += f"Agent_{message.sender.name} : {message.message}\n"
            else:
                prompt += f"Human : {message.message}\n"
        return prompt

    def get_entity_dialog(self, entity: str):
        dialog = [
            message.message for message in self.messages if message.sender == entity
        ]
        return dialog
