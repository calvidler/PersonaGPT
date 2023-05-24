import sqlite3
import datetime
import json
import os
import threading

from models import Actions


class WordDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()
        self.load_agents_from_config()

    def get_conn(self):
        return sqlite3.connect(self.db_file)

    def disconnect(self, conn):
        if conn:
            conn.close()

    def create_tables(self):
        agents_table_query = """
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                bio TEXT,
                traits TEXT,
                goals TEXT,
                active INTEGER,
                system TEXT,
                voice TEXT
            )
        """

        dialog_table_query = """
            CREATE TABLE IF NOT EXISTS dialog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                recipient TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        actions_table_query = """
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """

        conn = self.get_conn()
        with conn:
            conn.execute(agents_table_query)
            conn.execute(dialog_table_query)
            conn.execute(actions_table_query)
        self.disconnect(conn)

    def load_agents_from_config(self):
        query = """
            SELECT COUNT(*) FROM agents
        """
        conn = self.get_conn()
        with conn:
            cursor = conn.execute(query)
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
                            agent["system"],
                            agent["voice"],
                        )
        self.disconnect(conn)

    def insert_agent(self, name, bio, traits, goals, active, system, voice):
        query = """
            INSERT INTO agents (name, bio, traits, goals, active, system, voice)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        conn = self.get_conn()
        with conn:
            conn.execute(
                query,
                (
                    name,
                    bio,
                    json.dumps(traits),
                    json.dumps(goals),
                    active,
                    system,
                    voice,
                ),
            )
        self.disconnect(conn)

    def insert_dialog(self, sender, recipient, message):
        query = """
            INSERT INTO dialog (sender, recipient, message)
            VALUES (?, ?, ?)
        """

        conn = self.get_conn()
        with conn:
            conn.execute(query, (sender, recipient, message))
        self.disconnect(conn)

        self.insert_action(sender, Actions.SPOKE.value)

    def update_agent_status(self, agent_id, active):
        query = """
            UPDATE agents SET active = ? WHERE id = ?
        """

        conn = self.get_conn()
        with conn:
            conn.execute(query, (active, agent_id))
        self.disconnect(conn)
        # adding a new action
        if active == 1:
            self.insert_action(agent_id, Actions.ACTIVATE.value)
        else:
            self.insert_action(agent_id, Actions.DEACTIVATE.value)

    def get_agents(self):
        query = """
            SELECT id, name, bio, traits, goals, active, system, voice
            FROM agents
        """
        new_agents = []

        conn = self.get_conn()
        with conn:
            cursor = conn.execute(query)
            agents = cursor.fetchall()
            for agent in agents:
                id, name, bio, traits, goals, active, system, voice = agent
                goals = json.loads(goals)
                traits = json.loads(traits)
                new_agents.append((id, name, bio, traits, goals, active, system, voice))
        self.disconnect(conn)
        return new_agents

    def get_dialog(self):
        query = """
            SELECT d.id, d.sender, d.recipient, d.message, d.timestamp
            FROM dialog d
        """

        conn = self.get_conn()
        dialogs = []
        with conn:
            cursor = conn.execute(query)
            dialogs = cursor.fetchall()
        self.disconnect(conn)
        return dialogs

    def get_agent_dialog(self, agent_id):
        query = """
            SELECT d.id, d.sender, d.recipient, d.message, d.timestamp
            FROM dialog d
            WHERE d.sender = ?
        """

        conn = self.get_conn()
        dialogs = []
        with conn:
            cursor = conn.execute(query, (str(agent_id),))
            dialogs = cursor.fetchall()
        self.disconnect(conn)

        return dialogs

    def get_human_dialog(self):
        query = """
            SELECT d.id, d.sender, d.recipient, d.message, d.timestamp
            FROM dialog d
            WHERE d.sender = 'human'
        """

        conn = self.get_conn()
        dialogs = []
        with conn:
            cursor = conn.execute(query)
            dialogs = cursor.fetchall()
        self.disconnect(conn)

        return dialogs

    def insert_action(self, entity, action):
        query = """
            INSERT INTO actions (entity, action)
            VALUES (?, ?)
        """

        conn = self.get_conn()
        with conn:
            conn.execute(query, (entity, action))
        self.disconnect(conn)

    def get_actions(self):
        query = """
            SELECT id, entity, action, timestamp
            FROM actions
        """

        conn = self.get_conn()
        actions = []
        with conn:
            cursor = conn.execute(query)
            actions = cursor.fetchall()
        self.disconnect(conn)
        return actions
