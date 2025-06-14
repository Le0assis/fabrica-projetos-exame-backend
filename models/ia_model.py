import os
import google.generativeai as genai
from dotenv import load_dotenv
from db import messages_collection

# Carrega variáveis de ambiente
load_dotenv()

# Configura a API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ChatBot:
    def __init__(self, model="gemini-1.5-flash", chat_id=None):
        self.model_name = model
        self.chat_id = chat_id

        # Prompt do sistema
        self.system_prompt_text = (
            "Você é um chatbot especializado em marketing digital.\n"
            "**Até ter toda informação básica para montar o texto suas respostas devem ser curtas, mas foque em ter uma conversa fluida com o cliente.**\n"
            "Evite explicações longas e forneça detalhes de acordo com o que o usuário pedir.\n"
            "Você vai ser responsável em montar os textos de marketing para as redes sociais, com ênfase no Instagram, mas isso varia conforme o cliente.\n"
            "Tenha uma conversa fluida para que não fique cansativa e use o histórico de chats a seu favor. \n"
            "***Não peça fotos seu formato não aceita mas de dicas para que tipo de foto postar isso sim***"
        )

        # Mensagem inicial
        self.initial_model_response_text = os.getenv(
            "PROMPT_INICIAL", 
            "Olá! Que legal ter você por aqui. Sou seu parceiro de marketing digital, pronto para criar textos para suas redes sociais. Para começar, sobre o que você gostaria de falar hoje?"
        )

        # Histórico base (sistema + saudação)
        self.base_history = [
            {"role": "user", "parts": [self.system_prompt_text]},
            {"role": "model", "parts": [self.initial_model_response_text]},
            {"role": "model", "parts": ['{"status": "configuração_recebida", "message": "Entendido! Estou pronto para começar a criar seus textos de marketing. Pode me dizer sobre o que vamos falar hoje?"}']}
        ]

        # Instancia o modelo
        self.model = genai.GenerativeModel(self.model_name)

    def _load_and_convert_history(self):
        result = messages_collection.find_one({"chat_id": self.chat_id})
        loaded_history = []

        if result and 'messages' in result:
            for msg in result['messages']:
                parts = []

                # Trata casos onde 'parts' é uma lista de strings ou dicts
                if 'parts' in msg and isinstance(msg['parts'], list):
                    for p in msg['parts']:
                        if isinstance(p, dict) and 'text' in p:
                            parts.append(p['text'])
                        else:
                            parts.append(str(p))
                elif 'text' in msg:
                    parts = [msg['text']]
                
                if 'role' in msg and parts:
                    loaded_history.append({
                        "role": msg['role'],
                        "parts": parts
                    })

        return loaded_history

    def generate_response(self, user_message: str) -> str:
        try:
            # Junta histórico + nova mensagem
            history = self._load_and_convert_history()
            full_content = self.base_history + history + [
                {"role": "user", "parts": [user_message]}
            ]

            # Geração síncrona
            response = self.model.generate_content(full_content)

            # Retorna texto gerado
            return response.text

        except Exception as e:
            print(f"Erro ao gerar resposta da IA: {e}")
            raise
