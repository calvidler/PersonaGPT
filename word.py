# World class
import datetime
import random
from fastapi import HTTPException
from agent import Agent
from llm import LLM
from services.db import WordDatabase


# World class
class World:
    def __init__(self, db_file):
        self.db = WordDatabase(db_file)
        self.agents = self.load_agents_from_database()

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
            )
            agents.append(agent)
        return agents

    def get_active_agents(self):
        active_agents = [agent for agent in self.agents if agent.active == 1]
        return active_agents

    def deactivate_agent(self, agent_id):
        query = """
            UPDATE agents SET active = 0 WHERE id = ?
        """

        with self.db.conn:
            self.db.conn.execute(query, (agent_id,))

        for agent in self.agents:
            if agent.id == agent_id:
                agent.active = 0
                break

    def get_all_agents(self):
        return self.agents

    def query_agent(self, query):
        active_agents = self.get_active_agents()
        if len(active_agents) == 0:
            raise HTTPException(status_code=400, detail="No active agents available.")

        # Randomly select an active agent
        agent = random.choice(active_agents)

        # Use the LLM class to generate a response from ChatGPT
        llm = LLM()
        response = llm.generate_response(query)

        # Insert the dialog into the database
        self.db.insert_dialog(agent.id, query)
        self.db.insert_dialog(agent.id, response)

        return {
            "agent_id": agent.id,
            "agent_name": agent.name,
            "query": query,
            "response": response,
            "timestamp": str(datetime.datetime.now()),
        }
