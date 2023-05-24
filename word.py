# World class
import datetime
import random
from typing import List
from fastapi import HTTPException
from coversation import Conversation, Message
from llm import LLM
from agent import Agent
from models import Entity
from services.db import WordDatabase


# World class
class World:
    def __init__(self, db_file):
        self.db = WordDatabase(db_file)
        self.agents: List[Agent] = self.load_agents_from_database()
        self.llm = LLM()

    def load_agents_from_database(self):
        agents_data = self.db.get_agents()
        agents = []
        for agent_data in agents_data:
            agent = Agent(
                id=agent_data[0],
                name=agent_data[1],
                bio=agent_data[2],
                traits=agent_data[3],
                goals=agent_data[4],
                active=agent_data[5],
                system=agent_data[6],
                voice=agent_data[7],
            )
            agents.append(agent)
        return agents

    @property
    def conversation(self) -> Conversation:
        # TODO clean all this garbage up eww
        conversation = Conversation()
        for dialog in self.get_dialog_history():
            message = Message(
                sender=dialog["sender"],
                message=dialog["message"],
                timestamp=dialog["timestamp"],
            )
            conversation.add_message(message)
        return conversation

    def get_active_agents(self):
        active_agents = [agent for agent in self.agents if agent.active == 1]
        return active_agents

    def update_agent_status(self, agent_id, active):
        self.db.update_agent_status(agent_id, active)

    def deactivate_agent(self, agent_id):
        self.update_agent_status(agent_id, 0)

    def activate_agent(self, agent_id):
        self.update_agent_status(agent_id, 1)

    def get_all_agents(self):
        return self.agents

    def get_agent(self, agent_id: str) -> Agent:
        agent = next((agent for agent in self.agents if agent.id == agent_id), None)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found.")
        return agent

    def query_agent(self, query, agent_id=None):
        if agent_id is not None:
            agent = next((agent for agent in self.agents if agent.id == agent_id), None)
            if agent is None:
                raise HTTPException(status_code=404, detail="Agent not found.")
        else:
            active_agents = self.get_active_agents()
            if len(active_agents) == 0:
                raise HTTPException(
                    status_code=400, detail="No active agents available."
                )
            agent = random.choice(active_agents)

        messages: List[str] = agent.generate_messages(query, self.conversation)
        print([message.dict() for message in messages])
        response = self.llm.generate_response(messages)

        self.db.insert_dialog(
            str(Entity.HUMAN.value), str(agent.id), query
        )  # human is the sender of query!
        self.db.insert_dialog(str(agent.id), str(Entity.HUMAN.value), response)

        return {
            "agent_id": agent.id,
            "agent_name": agent.name,
            "query": query,
            "response": response,
            "timestamp": str(datetime.datetime.now()),
        }

    def query_all_agents(self, query):
        # TODO - implement a method to decide who responds to this message not all agents!
        responses = []
        for agent in self.agents:
            response = self.query_agent(query, agent.id)
            self.db.insert_dialog(
                str(Entity.HUMAN.value), str(Entity.EVERYONE.value), query
            )  # human is the sender of query!

            self.db.insert_dialog(str(agent.id), str(Entity.EVERYONE.value), response)
            responses.append(response)
        return responses

    def _get_entity(self, entity_name: str):
        for agent in self.agents:
            if str(agent.id) == entity_name:
                return agent
        return entity_name

    def get_dialog_history(self):
        dialogs = self.db.get_dialog()
        dialog_history = []
        for dialog in dialogs:
            dialog_id, sender, reciever, message, timestamp = dialog

            dialog_history.append(
                {
                    "dialog_id": dialog_id,
                    "sender": self._get_entity(sender),
                    "reciever": self._get_entity(reciever),
                    "message": message,
                    "timestamp": timestamp,
                }
            )
        return dialog_history

    def get_agent_dialog_history(self, agent_id):
        agent = next((agent for agent in self.agents if agent.id == agent_id), None)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found.")

        dialog_history = self.db.get_agent_dialog(agent_id)
        response = []
        for dialog in dialog_history:
            print(dialog)
            dialog_id, agent_id, agent_name, message, timestamp = dialog
            response.append(
                {
                    "dialog_id": dialog_id,
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "message": message,
                    "timestamp": timestamp,
                }
            )
        return response

    def get_human_dialog_history(self):
        dialog_history = self.db.get_human_dialog()
        return dialog_history

    def get_actions(self):
        actions = self.db.get_actions()
        return actions
