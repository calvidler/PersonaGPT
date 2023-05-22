from enum import Enum
from typing import List, Union, Any
from pydantic import BaseModel

from models import ChatGPTMessage, ChatGPTRoles


class Message(BaseModel):
    sender: Union[Any, str]
    message: str
    timestamp: str

    def __init__(self, **args):
        super().__init__(**args)


class Conversation:
    messages: list[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def to_chatgpt_messages(self, skip_messages=0) -> List[ChatGPTMessage]:
        messages: List[ChatGPTMessage] = []
        sorted_messages = sorted(self.messages, key=lambda x: x.timestamp)

        # Skip messages from the start if skip_messages > 0
        messages_to_skip = min(skip_messages, len(sorted_messages))
        sorted_messages = sorted_messages[messages_to_skip:]

        for message in sorted_messages:
            if type(message.sender) != str:
                chatgpt_message = ChatGPTMessage(
                    role=ChatGPTRoles.ASSISTANT,
                    content=f"{message.sender.name} : {message.message}",
                )
                messages.append(chatgpt_message)
            else:
                chatgpt_message = ChatGPTMessage(
                    role=ChatGPTRoles.USER,
                    content=f"{message.message}",
                )
                messages.append(chatgpt_message)
        return messages

    def to_string(self, skip_messages=0):
        prompt = ""
        sorted_messages = sorted(self.messages, key=lambda x: x.timestamp)

        # Skip messages from the start if skip_messages > 0
        messages_to_skip = min(skip_messages, len(sorted_messages))
        sorted_messages = sorted_messages[messages_to_skip:]

        for message in sorted_messages:
            if type(message.sender) == str:
                prompt += f"Human : {message.message}\n"
            else:
                prompt += f"Agent_{message.sender.name} : {message.message}\n"
        return prompt

    def get_entity_dialog(self, entity: str):
        dialog = [
            message.message for message in self.messages if message.sender == entity
        ]
        return dialog
