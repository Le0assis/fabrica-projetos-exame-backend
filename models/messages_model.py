from datetime import datetime 

class Message:
    def __init__ (self, db):
        #É o que vai salva no db
        self.collection = db["messages"]

    def add_message(self, chat_id: str, role: str, content: str):
        doc = {
            'chat_id': chat_id,
            'role': role,
            'content': content,
            'horario': datetime.utcnow()
        }
        return self.collection.update_one(
            {"chat_id": chat_id},
            {"$push": {"messages": doc}},  # Adiciona a mensagem ao histórico
            upsert=True  # Cria um novo documento se o chat_id não for encontrado
        )
    
    def get_history (self, chat_id:str):
        return(
            self.collection.find({"chat_id": chat_id}).sort("horario", 1)
        )