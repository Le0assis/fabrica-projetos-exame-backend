import streamlit as st
import json
from models.ia_model import ChatBot

st.set_page_config(page_title="Chat com IA", page_icon="🤖", layout="centered")
st.title("ChatBot Eficaz")


if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

if "resposta" not in st.session_state:
    st.session_state.resposta = ""

def extrair_mensagem(texto):
    try:
        dados = json.loads(texto)
        return dados.get("message", texto)
    except json.JSONDecodeError:
        return texto

with st.form("form_pergunta", clear_on_submit=True):
    pergunta = st.text_input("Digite sua pergunta:")
    enviar = st.form_submit_button("Enviar")

# Processamento da resposta
if enviar and pergunta.strip():
    st.session_state.bot.add_user_message(pergunta)
    resposta = st.session_state.bot.generate_response()
    st.session_state.resposta = extrair_mensagem(resposta) 

# Exibe resposta da IA
st.text_area("Resposta da IA:", value=st.session_state.resposta, height=100, disabled=True)
