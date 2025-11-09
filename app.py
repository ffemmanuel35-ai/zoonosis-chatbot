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
API_URL = "https://router.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_KEY = st.secrets["general"]["hf_api_key"]  # ✅ Asegurate de tenerlo en Streamlit Secrets

def responder_hf(historial):
    """Envía el historial al modelo remoto de Hugging Face."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

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
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"].split("Asistente:")[-1].strip()
            elif "generated_text" in result:
                return result["generated_text"]
            else:
                return str(result)
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
