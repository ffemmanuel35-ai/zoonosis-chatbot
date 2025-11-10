import streamlit as st
import requests

# 🧠 Configuración del modelo Hugging Face (gratuito y compatible)
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_KEY = st.secrets["general"]["hf_api_key"]

headers = {"Authorization": f"Bearer {API_KEY}"}

st.set_page_config(page_title="Carla - Chatbot de Zoonosis", page_icon="🐾", layout="centered")

st.title("🐾 Carla - Asistente Virtual de Zoonosis")

st.markdown(
    "¡Hola! Soy **Carla**, tu asistente virtual. Puedo ayudarte con información sobre zoonosis, vacunación y cuidado animal. 🐶🐱"
)

# Guardar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje aquí...")

if prompt:
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Enviar a la API de Hugging Face
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            bot_reply = data[0]["generated_text"]
        except Exception:
            bot_reply = "Lo siento, ocurrió un error procesando la respuesta."
    else:
        bot_reply = f"⚠️ Error al conectar con Hugging Face: {response.status_code}"

    # Mostrar respuesta del bot
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
