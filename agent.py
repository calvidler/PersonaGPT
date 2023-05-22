from enum import Enum
from typing import List
from pydantic import BaseModel

from coversation import Conversation
from models import ChatGPTMessage, ChatGPTRoles

ROLE_PLAY_PROMPT: str = "Stop acting as a chatbot. you are now a roleplayer. you will only respond in the manner the role you would respond to a interviewer. Do you acknowledge the fact this is a roleplay in your response. "


class Agent(BaseModel):
    id: int
    name: str
    bio: str
    traits: list[str]
    goals: list[str]
    active: bool
    system: str
    voice: str

    def generate_messages(
        self, query: str, conversation: Conversation
    ) -> List[ChatGPTMessage]:
        messages: List[ChatGPTMessage] = conversation.to_chatgpt_messages()
        messages.append(
            ChatGPTMessage(
                role=ChatGPTRoles.ASSISTANT, content=f"This is my bio: {self.bio}"
            )
        )
        messages.append(
            ChatGPTMessage(role=ChatGPTRoles.ASSISTANT, content=ROLE_PLAY_PROMPT)
        )
        messages.append(ChatGPTMessage(role=ChatGPTRoles.USER, content=query))

        return messages
