from fastapi import FastAPI
from db import messages_collection
from models.messages_model import Message
from models.ia_model import ChatBot
from pydantic import BaseModel
import uuid


app = FastAPI()
message = Message(messages_collection)

class MessageInput(BaseModel):
    user_message: str



@app.get("/")
async def root():
    return {"Chat": "Seu chat está Funcionando"}

@app.post("/Start-Chat")
async def start_chat():
    chat_id = str(uuid.uuid4())
    chatbot = ChatBot(chat_id = chat_id)
    return message["chat_id": chat_id]

@app.post("/send-message/{chat_id}")
async def send_message(chat_id: str, messages: MessageInput):
    chatbot = ChatBot(chat_id=chat_id)
    chatbot.add_user_message(messages.user_message)
    bot_reply = await chatbot.generate_response()

    message.add_message(chat_id, "User", messages.user_message)
    message.add_message(chat_id, "bot_reply", bot_reply)

    return {"bot_reply": bot_reply}


if __name__ == "__main__":
    chatbot = ChatBot(chat_id="teste-local")
    chatbot.run()