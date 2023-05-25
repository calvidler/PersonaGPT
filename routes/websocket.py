from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
import time
from config import world
from datetime import datetime
import asyncio
import httpx

websocket_router = APIRouter()

chats = {""}


async def send_message(username: str, message: str, chat: str):
    url = f"https://api.chatengine.io/chats/{chat}/messages/"
    headers = {
        "Project-ID": "35a498c6-01f5-407b-92e5-d923655e1441}",
        "User-Name": username,
        "User-Secret": username,
    }
    data = {"text": message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        # response.raise_for_status()
        return response.json()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def agent_listen(
        self, agent_id: str, websocket: WebSocket, last_message_returned=None
    ):
        await asyncio.sleep(1)

        conversation = world.get_agent_dialog_history(int(agent_id))

        if len(conversation) == 0:
            return

        sorted_conversation = sorted(
            conversation,
            key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"),
        )

        last_message = sorted_conversation[-1]["message"]

        if last_message_returned is None or last_message_returned == last_message:
            print("Agent is silent, waiting...")
            # await self.send(f"Agent is silent", websocket)
            return last_message

        print(f"Agent has answered: {last_message}")
        await self.send(f"{last_message}", websocket)
        await send_message("Darth Vader", last_message, "175478")

        return last_message

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            agent_id = await websocket.receive_text()

            # agent_id = agent_id["agent_id"]

            await manager.send(f"Talking to {agent_id}", websocket)
            # await manager.broadcast(f"Broadcast: {agent_id}")

            last_message = None
            while True:
                last_message = await manager.agent_listen(
                    agent_id, websocket, last_message
                )

        except Exception as e:
            print(f"WebSocket connection closed: {e}")
            break


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@websocket_router.get("/ws/test")
async def test_websocket_endpoint():
    return HTMLResponse(html)
