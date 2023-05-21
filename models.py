from pydantic import BaseModel
from openai import ChatCompletion


class Agent(BaseModel):
    id: int
    name: str
    bio: str
    traits: list[str]
    goals: list[str]
    active: bool


class LLMParser:
    def __init__(self):
        # Initialize the OpenAI ChatCompletion instance
        self.chat_completion = ChatCompletion()

    def parse_query(self, query: str) -> str:
        # Send the query to ChatGPT for completion
        response = self.chat_completion.complete_message(query)

        # Extract the generated response from the OpenAI response
        reply = response["choices"][0]["message"]["content"]

        return reply


class Discord:
    def __init__(self, agent: Agent, query: str, llm_parser: LLMParser = LLMParser()):
        self.agent = agent
        self.query = query
        self.llm_parser = llm_parser

    def query_chatgpt(self):
        # Customize the template for querying ChatGPT
        template = (
            f"Agent: {self.agent.name}\n"
            f"Bio: {self.agent.bio}\n"
            f"Traits: {', '.join(self.agent.traits)}\n"
            f"Goals: {', '.join(self.agent.goals)}\n"
            f"User Query: {self.query}\n"
        )

        # Prepare the input by concatenating the template and the query
        input_text = template + self.query

        # Use the LLMParser to send the query to ChatGPT
        response = self.llm_parser.parse_query(input_text)

        return response
