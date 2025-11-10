import streamlit as st
from transformers import pipeline
from googletrans import Translator

# -----------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------
st.set_page_config(
    page_title="CarlaTL - Asistente de Zoonosis",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 Carla - Asistente Virtual de Zoonosis")
st.markdown(
    "¡Hola! Soy **Carla**, tu asistente virtual. 🐶🐱<br>"
    "Puedo ayudarte con información sobre **zoonosis, vacunación, prevención y cuidado animal**.",
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# CARGAR MODELO (TinyLlama)
# -----------------------------------------------------------
@st.cache_resource
def cargar_modelo():
    try:
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        st.info(f"Cargando modelo `{model_name}`... Puede tardar unos segundos ⏳")
        model = pipeline("text-generation", model=model_name)
        st.success("✅ Modelo cargado correctamente.")
        return model
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {e}")
        return None

nlp = cargar_modelo()
translator = Translator()

# -----------------------------------------------------------
# CONTEXTO DEL CHATBOT
# -----------------------------------------------------------
contexto = (
    "Eres Carla, una asistente virtual especializada en zoonosis, vacunación y cuidado animal. "
    "Brindas información confiable y clara sobre prevención de enfermedades, campañas de vacunación, "
    "cuidados veterinarios y tenencia responsable de mascotas. Respondes siempre en español y con un tono amable."
)

if "historial" not in st.session_state:
    st.session_state.historial = ""

# -----------------------------------------------------------
# FUNCIÓN DE RESPUESTA
# -----------------------------------------------------------
def responder(texto_es):
    if not texto_es.strip():
        return "Por favor, escribí una pregunta o mensaje."

    # Traducir al inglés (TinyLlama fue entrenado principalmente en inglés)
    texto_en = translator.translate(texto_es, src='es', dest='en').text

    prompt_en = (
        f"{contexto}\n\n"
        f"Previous conversation:\n{st.session_state.historial}\n\n"
        f"User: {texto_en}\nAssistant:"
    )

    try:
        generacion = nlp(
            prompt_en,
            max_new_tokens=60,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            num_return_sequences=1
        )[0]
        respuesta_en = generacion['generated_text'][len(prompt_en):].strip()
    except Exception as e:
        respuesta_en = "I'm not sure how to respond to that."
        st.error(f"⚠️ Error interno del modelo: {e}")

    # Traducir respuesta al español
    respuesta_es = translator.translate(respuesta_en, src='en', dest='es').text

    # Actualizar historial
    st.session_state.historial += f"\nUsuario: {texto_es}\nCarla: {respuesta_es}"
    return respuesta_es

# -----------------------------------------------------------
# INTERFAZ DE CHAT
# -----------------------------------------------------------
user_input = st.text_input("💬 Escribí tu consulta aquí:")

if st.button("Enviar"):
    if nlp:
        respuesta = responder(user_input)
        st.markdown(f"**🐾 Carla:** {respuesta}")
    else:
        st.error("El modelo no se pudo cargar correctamente.")

# Mostrar historial opcional
with st.expander("🧠 Ver historial de conversación"):
    st.text(st.session_state.historial)
