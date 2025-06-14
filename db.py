from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

try: 
    client = MongoClient(MONGO_URL)
    db = client["chatdb"]  # Nome do banco
    messages_collection = db["messages"]  # Coleção de mensagens
    print("Mensagem enviada")

except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    db = None
