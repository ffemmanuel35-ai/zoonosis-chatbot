import streamlit as st
import requests

# ======================================================
# 🐾 CONFIGURACIÓN DE LA APP
# ======================================================
st.set_page_config(page_title="Asistente de Zoonosis", page_icon="🐾")
st.title("🐾 Carla — Asistente Virtual de Zoonosis 🐶🐱")

st.markdown("""
Soy **Carla**, tu asistente de Zoonosis Municipal.  
Puedo informarte sobre:
- 📅 Días y horarios de castración  
- 📍 Lugares donde se realizan  
- 🐕 Cuidados pre y post operatorios  
- 💚 Beneficios de castrar  
- 📞 Cómo pedir turnos o contactarte  
""")

# ======================================================
# ⚙️ CONFIGURACIÓN DE HUGGING FACE
# ======================================================
API_URL = "https://router.huggingface.co/hf-inference/models/microsoft/Phi-3-mini-4k-instruct"
API_KEY = st.secrets["general"]["hf_api_key"]  # ✅ coincide con el formato del Secret en Streamlit

def responder_hf(historial):
    """Envía el historial al modelo remoto de Hugging Face."""
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Convertimos el historial en un único texto (estilo chat)
    prompt = "\n".join([
        f"{'Usuario' if m['role'] == 'user' else 'Asistente'}: {m['content']}"
        for m in historial
    ]) + "\nAsistente:"

    data = {"inputs": prompt, "parameters": {"max_new_tokens": 250}}

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            # Algunos modelos devuelven lista, otros texto directo
            return result[0]["generated_text"].split("Asistente:")[-1].strip()
        except Exception:
            return str(result)
    else:
        return f"⚠️ Error al conectar con Hugging Face: {response.status_code} - {response.text}"


# ======================================================
# 💬 CHAT
# ======================================================
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy Carla, tu asistente de Zoonosis. ¿En qué puedo ayudarte hoy?"}
    ]

# Campo para ingresar texto
pregunta = st.chat_input("Escribí tu pregunta aquí...")

# Procesar pregunta
if pregunta:
    st.session_state.historial.append({"role": "user", "content": pregunta})

    try:
        respuesta = responder_hf(st.session_state.historial)
    except Exception as e:
        respuesta = f"⚠️ Error al generar respuesta: {e}"

    st.session_state.historial.append({"role": "assistant", "content": respuesta})

# Mostrar historial del chat
for msg in st.session_state.historial:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 **Tú:** {msg['content']}")
    else:
        st.markdown(f"🐾 **Carla:** {msg['content']}")
