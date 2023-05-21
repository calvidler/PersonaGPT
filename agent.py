# Agent class using BaseModel
from typing import List
from pydantic import BaseModel


class Agent(BaseModel):
    id: int
    name: str
    bio: str
    traits: List[str]
    goals: List[str]
    active: int


def generate_prompt(self, query):
    return f"Agent Name: {self.name}\nQuery: {query}"
