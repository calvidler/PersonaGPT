# LLM class
from coversation import Conversation
from models import Agent

ROLE_PLAY_PROMPT: str = "Stop acting as a chatbot. you are now a roleplayer. you will only respond in the manner the role you would respond to a interviewer. Do you acknowledge the fact this is a roleplay in your response. "

class LLM:
    # TODO move into agent to generate prompt!
    # TODO add choosing a model from config ect.
    def generate_response(self, prompt: str, agent: Agent, conversation: Conversation):
        # Placeholder implementation, replace with actual ChatGPT interaction
        print(conversation.to_string())
        response = "This is a response from ChatGPT."
        print(agent.system)
        return response
