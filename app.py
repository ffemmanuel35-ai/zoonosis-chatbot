import streamlit as st
from collections import deque

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente de Zoonosis", page_icon="🐾")
st.title("🐾 Carla — Asistente Virtual de Zoonosis 🐶🐱")

st.markdown("""
Soy **Carla**, tu asistente de Zoonosis Municipal de **Termas de Río Hondo, Santiago del Estero**.  
Puedo informarte sobre:
- 📅 Horarios y lugares de castración  
- 🐾 Cuidados pre y post operatorios  
- 💚 Beneficios y edades recomendadas  
- 🏥 Procedimiento y cantidad diaria de castraciones  
""")

# --- CARGAR INFORMACIÓN LOCAL ---
def cargar_info():
    try:
        with open("info_zoonosis.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ No se encontró el archivo de información local."

info_local = cargar_info().lower()

# --- FUNCIÓN PARA BUSCAR EN INFORMACIÓN LOCAL Y VALIDAR ESPECIES ---
def buscar_respuesta_local(pregunta):
    pregunta = pregunta.lower()
    
    # --- Validar especies ---
    animales_prohibidos = ["conejo", "hurón", "loro", "cobayo"]  # se puede ampliar
    for animal in animales_prohibidos:
        if animal in pregunta:
            return "❌ Solo se castran perros y gatos en Zoonosis."

    # --- Búsqueda en info local según palabras clave ---
    claves = {
        "horario": "horario de castración",
        "hora": "horario de castración",
        "mañana": "horario de castración",
        "lugar": "lugares de castración",
        "dónde": "lugares de castración",
        "direccion": "lugares de castración",
        "cuidados": "cuidados pre y post operatorios",
        "preoperatorio": "cuidados pre y post operatorios",
        "postoperatorio": "cuidados pre y post operatorios",
        "ventajas": "ventajas de la castración",
        "beneficios": "ventajas de la castración",
        "edad": "edad recomendada",
        "procedimiento": "procedimiento de castración",
        "especie": "especies que se castran",
        "cuantos": "cantidad diaria de castraciones",
        "turno": "orden de llegada"
    }

    for clave, tema in claves.items():
        if clave in pregunta:
            inicio = info_local.find(tema.lower())
            if inicio != -1:
                fin = info_local.find("\n\n", inicio)
                if fin == -1:
                    fin = len(info_local)
                return info_local[inicio:fin].strip().capitalize()
    return "Lo siento, no tengo información sobre ese tema. Podés preguntar por horarios, lugares o cuidados de castración."

# --- HISTORIAL (MEMORIA DE CONTEXTO) ---
if "historial" not in st.session_state:
    st.session_state.historial = deque(maxlen=6)
    st.session_state.historial.append(
        {"role": "assistant", "content": "¡Hola! 👋 Soy Carla, asistente de Zoonosis. ¿En qué puedo ayudarte hoy?"}
    )

# --- CAMPO DE ENTRADA ---
pregunta = st.chat_input("Escribí tu pregunta aquí...")

# --- PROCESAR PREGUNTA ---
if pregunta:
    st.session_state.historial.append({"role": "user", "content": pregunta})

    # Buscar respuesta en la información local
    respuesta = buscar_respuesta_local(pregunta)

    # Guardar respuesta
    st.session_state.historial.append({"role": "assistant", "content": respuesta})

# --- MOSTRAR HISTORIAL ---
for msg in st.session_state.historial:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 **Tú:** {msg['content']}")
    else:
        st.markdown(f"🐾 **Carla:** {msg['content']}")
