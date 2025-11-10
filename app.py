import streamlit as st
import requests

# ======================================================
# 🧠 CONFIGURACIÓN DE HUGGING FACE (NUEVO ENDPOINT)
# ======================================================
API_URL = "https://api.huggingface.co/models/google/gemma-2b-it"  # ✅ modelo activo
API_KEY = st.secrets["general"]["hf_api_key"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ======================================================
# 🐾 INTERFAZ DE USUARIO
# ======================================================
st.set_page_config(page_title="Carla - Asistente Virtual de Zoonosis", page_icon="🐾", layout="centered")
st.title("🐾 Carla - Asistente Virtual de Zoonosis")
st.markdown("""
¡Hola! Soy **Carla3**, tu asistente virtual.  
Puedo ayudarte con información sobre zoonosis, vacunación y cuidado animal. 🐶🐱
""")

# Guardar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================================================
# 💬 INTERACCIÓN
# ======================================================
prompt = st.chat_input("Escribí tu mensaje aquí...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 250, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                reply = data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                reply = data["generated_text"]
            else:
                reply = "Lo siento, no pude generar una respuesta."
        else:
            reply = f"⚠️ Error al conectar con Hugging Face: {response.status_code} - {response.text}"

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
