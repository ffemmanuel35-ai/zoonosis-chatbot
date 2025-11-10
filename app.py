import streamlit as st
import requests

# 🧠 Configuración del modelo Hugging Face (nuevo endpoint)
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/blenderbot-400M-distill"
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

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje aquí...")

if prompt:
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Enviar solicitud al nuevo endpoint
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                bot_reply = data[0]["generated_text"]
            else:
                bot_reply = "Lo siento, no pude generar una respuesta."
        else:
            bot_reply = f"⚠️ Error al conectar con Hugging Face: {response.status_code}"

    except Exception as e:
        bot_reply = f"⚠️ Error al procesar la solicitud: {str(e)}"

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
