from fastapi import FastAPI
from db import messages_collection
from models.messages_model import Message
from models.ia_model import ChatBot
from pydantic import BaseModel
import uuid


app = FastAPI()
messages = Message(messages_collection)

class Message(BaseModel):
    user_message: str



@app.get("/")
async def root():
    return {"Chat"}

@app.post("/Start-Chat")
async def start_chat():
    chat_id = str(uuid.uuid4())
    chatbot = ChatBot(chat_id = chat_id)
    return {"chat_id": chat_id}

@app.post("/send-message/{chat_id}")
async def send_message(chat_id: str, message: Message):
    chatbot = ChatBot(chat_id=chat_id)
    chatbot.add_user_message(message.user_message)
    bot_reply = chatbot.generate_response()

    messages.add_message(chat_id, "User", message.user_message)
    message.add_message(chat_id, "bot_reply", bot_reply)

    return {"bot_response": bot_reply}

@app.post("/chat")
def send_message (chat_id: str, content:str):
    messages.add_message(chat_id, "user", content)
    bot_reply = f"Você disse: {content}"
    messages.add_message(chat_id, "reply", bot_reply)
    return {'reply': bot_reply}    

chatbot = ChatBot(chat_id=123)
chatbot.run()