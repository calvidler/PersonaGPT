import asyncio
from websockets.sync.client import connect

def init_agent(agent_id: int):
    with connect('ws://localhost:8000/ws') as websocket:
        
        # Send agent id
        websocket.send(str(agent_id))


        while True:
            response = websocket.recv()
            print(f"Response from server: {response}")

init_agent(1)