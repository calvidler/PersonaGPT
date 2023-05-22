from pydantic import BaseModel

from enum import Enum


class Actions(Enum):
    DEACTIVATE = "deactivate"
    ACTIVATE = "activate"
    SPOKE = "spoke"


class Entity(Enum):
    EVERYONE = "everyone"
    HUMAN = "human"
    # OR use agent id


class ChatGPTRoles(str, Enum):
    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"


class ChatGPTMessage(BaseModel):
    role: ChatGPTRoles
    content: str

    def dict(self, *args, **kwargs):
        return {"role": self.role.value, "content": self.content}
