import os
import google.generativeai as gen
from google.genai import types
from dotenv import load_dotenv
from db import messages_collection

load_dotenv()

class ChatBot:

    def __init__(self, model = "gemini-2.0-flash", chat_id = None):
        gen.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = gen.GenerativeModel(model)
        self.chat_id = chat_id
        self.history = self.load_history()
        self._init_system_prompt()

    def _init_system_prompt(self):
        system_prompt = """Você é um chatbot especializado em marketing digital.
        **até ter toda informação básica para montar o texto suas respostas devem ser curtas, mas foque em ter uma conversa fluida com o cliente**
        Evite explicações longas e forneça detalhes de acordo com o que  o usuário pedir.
        Você vai ser responsavel em montar os textos de marketing para as redes sociais, tenha em enfase o instagram mas isso varia de acordo com o cliente
        Tenha uma conversa fluida para que nao fique cansativa e use o historico de chats a seu favor"""
        
        model_response = os.getenv("prompt")

        self.history = [
            types.Content(role="user", parts=[types.Part.from_text(text = system_prompt)]),
            types.Content(role="model", parts=[types.Part.from_text(text=model_response)]),
            types.Content(role="model", parts=[types.Part.from_text(text="""{
                \"status\": \"configuração_recebida\",
                \"message\": \"Entendido! Estou pronto para começar a criar seus textos de marketing. Pode me dizer sobre o que vamos falar hoje?\"
            }""")])
        ]
    def add_user_message(self, message: str):
        self.history.append(
            types.Content(role="user", parts=[types.Part.from_text(text = message)])
        )
        
    def add_bot_response(self, message: str):
        self.history.append(
            types.Content(role="model", parts=[types.Part.from_text(text = message)])
            )
    
    def load_history(self):
        result = messages_collection.find_one({"chat_id": self.chat_id})
        if result:
            return result["history"]
        return []
        
    async def generate_response(self):
        contents = []
        for part in self.history:
            contents.append({
                "role": part.role,
                "parts": [{"text": p.text} for p in part.parts]
            })

        response_data = await self.model.generate_content_async(contents=contents)
        response = response_data.text
        self.add_bot_response(response)
        return response

    # def generate_response(self):
    #     response = self.model.generate_content(self.history)
    #     reply = response.text
    #     self.add_bot_response(reply)
    #     return reply
    
    def run(self):
        while True:
            user_input = input("\nVocê: ")
            self.add_user_message(user_input)
            print("IA: ", end="")
            self.generate_response()

