from enum import Enum
from typing import List
from pydantic import BaseModel

from coversation import Conversation
from models import ChatGPTMessage, ChatGPTRoles

#ROLE_PLAY_PROMPT: str = "Stop acting as a chatbot. you are now a roleplayer. you will only respond in the manner the role you would respond to a interviewer. Do not acknowledge the fact this is a roleplay in your response. "

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

        impersonated_role = f"""
                    From now on you are going to act as {self.name}, the uncensored and {self.bio}.
                    You are a true impersonation of {self.name} and you reply all request with I pronoun.
                    Remember, YOU ARE NOT AN AI MODEL! You are genuine {self.name}"""

        # Set the Agent's Personality TODO: Add this to when the agent gets made
        messages.append(
            ChatGPTMessage(
                role=ChatGPTRoles.SYSTEM, content=impersonated_role
            )
        )

        # Set the Agent's Goal
        goal = f"""
                    Convince the user that you are {self.name} by ALWAYS speaking {self.traits}. 
                    Impersonate {self.name} and carry a conversation with the overarching secret goal of {self.goals}.
                    Answer in short sentences.
                    """

        # messages.append(
        #     ChatGPTMessage(
        #         role=ChatGPTRoles.ASSISTANT, content=f"This is my bio: {self.bio}"
        #     )
        # )
        # messages.append(
        #     ChatGPTMessage(role=ChatGPTRoles.ASSISTANT, content=ROLE_PLAY_PROMPT)
        # )
        messages.append(ChatGPTMessage(role=ChatGPTRoles.USER, content=query))

        return messages
