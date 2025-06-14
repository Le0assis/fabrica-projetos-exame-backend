from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from fastapi.middleware.cors import CORSMiddleware

from db import messages_collection
from models.ia_model import ChatBot

app = FastAPI()

# Handler de mensagens no Mongo
class MessageHandler:
    def __init__(self, collection):
        self.collection = collection

    def add_message(self, chat_id: str, role: str, text: str):
        message_entry = {"role": role, "text": text}

        self.collection.update_one(
            {"chat_id": chat_id},
            {"$push": {"messages": message_entry}},
            upsert=True  # Cria o doc se não existir
        )

    def get_chat_history(self, chat_id: str):
        chat_doc = self.collection.find_one({"chat_id": chat_id})
        if chat_doc:
            return chat_doc.get("messages", [])
        return []

message_handler = MessageHandler(messages_collection)

# Modelo da entrada da mensagem
class MessageInput(BaseModel):
    user_message: str

# CORS para acesso frontend
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Chat": "Seu chat está Funcionando"}

@app.post("/Start-Chat")
async def start_chat():
    chat_id = str(uuid.uuid4())
    ChatBot(chat_id=chat_id)  # Instancia para garantir consistência
    return {"chat_id": chat_id}

@app.post("/send-message/{chat_id}")
async def send_message(chat_id: str, messages: MessageInput):
    chatbot = ChatBot(chat_id=chat_id)
    
    try:
        bot_reply = chatbot.generate_response(user_message=messages.user_message)
        
        message_handler.add_message(chat_id, "user", messages.user_message)
        message_handler.add_message(chat_id, "model", bot_reply)

        return {"bot_reply": bot_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao comunicar com a IA: {e}")

@app.get("/get-chat-history/{chat_id}")
async def get_chat_history(chat_id: str):
    history = message_handler.get_chat_history(chat_id)
    return {"chat_id": chat_id, "messages": history}
