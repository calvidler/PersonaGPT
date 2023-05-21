import sqlite3
import datetime
import json
import os


class WordDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.create_tables()
        self.load_agents_from_config()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self):
        agents_table_query = """
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                bio TEXT,
                traits TEXT,
                goals TEXT,
                active INTEGER
            )
        """

        dialog_table_query = """
            CREATE TABLE IF NOT EXISTS dialog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id INTEGER,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents (id)
            )
        """

        with self.conn:
            self.conn.execute(agents_table_query)
            self.conn.execute(dialog_table_query)

    def load_agents_from_config(self):
        query = """
            SELECT COUNT(*) FROM agents
        """
        cursor = self.conn.execute(query)
        count = cursor.fetchone()[0]
        if count == 0:
            with open("config.json") as f:
                config_data = json.load(f)
                for agent in config_data["agents"]:
                    self.insert_agent(
                        agent["name"],
                        agent["bio"],
                        agent["traits"],
                        agent["goals"],
                        agent["active"],
                    )

    def insert_agent(self, name, bio, traits, goals, active):
        query = """
            INSERT INTO agents (name, bio, traits, goals, active)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.conn:
            self.conn.execute(
                query, (name, bio, json.dumps(traits), json.dumps(goals), active)
            )

    def insert_dialog(self, agent_id, message):
        query = """
            INSERT INTO dialog (agent_id, message)
            VALUES (?, ?)
        """

        with self.conn:
            self.conn.execute(query, (agent_id, message))

    def deactivate_agent(self, agent_id):
        query = """
            UPDATE agents SET active = 0 WHERE id = ?
        """

        with self.conn:
            self.conn.execute(query, (agent_id,))

    def activate_agent(self, agent_id):
        query = """
            UPDATE agents SET active = 1 WHERE id = ?
        """

        with self.conn:
            self.conn.execute(query, (agent_id,))

    def get_agents(self):
        query = """
            SELECT id, name, bio, traits, goals, active
            FROM agents
        """

        with self.conn:
            cursor = self.conn.execute(query)
            agents = cursor.fetchall()
            new_agents = []
            for agent in agents:
                id, name, bio, traits, goals, active = agent
                goals = json.loads(goals)
                traits = json.loads(traits)
                new_agents.append((id, name, bio, traits, goals, active))
            print(new_agents)
            return new_agents

    def get_dialog(self):
        query = """
            SELECT d.id, a.name, d.message, d.timestamp
            FROM dialog d
            JOIN agents a ON d.agent_id = a.id
        """

        with self.conn:
            cursor = self.conn.execute(query)
            return cursor.fetchall()
