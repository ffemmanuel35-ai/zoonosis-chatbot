import streamlit as st
from collections import deque
import difflib
import datetime
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente de Zoonosis", page_icon="🐾", layout="centered")
st.title("🐾 Carla — Asistente Virtual de Zoonosis 🐶🐱")

st.markdown("""
Soy **Carla**, tu asistente virtual de Zoonosis Municipal de **Termas de Río Hondo, Santiago del Estero**.  
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

# --- FUNCIONES AUXILIARES ---
def guardar_pregunta_no_respondida(pregunta):
    """Guarda las preguntas sin respuesta en un archivo de log."""
    with open("preguntas_no_respondidas.log", "a", encoding="utf-8") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] {pregunta}\n")

def cargar_preguntas_pendientes():
    """Lee las preguntas sin respuesta."""
    if not os.path.exists("preguntas_no_respondidas.log"):
        return []
    with open("preguntas_no_respondidas.log", "r", encoding="utf-8") as f:
        return f.readlines()

# --- FUNCIÓN: BUSCAR RESPUESTA LOCAL ---
def buscar_respuesta_local(pregunta):
    pregunta = pregunta.lower()

    # --- Validar especies ---
    animales_prohibidos = ["conejo", "hurón", "hamster", "loro", "cobayo", "ave", "pájaro", "tortuga"]
    for animal in animales_prohibidos:
        if animal in pregunta:
            return "❌ Solo se castran perros y gatos en el área de Zoonosis."

    # --- Diccionario de palabras clave ---
    claves = {
        # Horarios
        "horario": "horario de castración",
        "hora": "horario de castración",
        "mañana": "horario de castración",
        "cuando": "horario de castración",
        "día": "horario de castración",
        "dias": "horario de castración",

        # Lugares
        "lugar": "lugares de castración",
        "dónde": "lugares de castración",
        "donde": "lugares de castración",
        "direccion": "lugares de castración",
        "hospital": "lugares de castración",
        "barrio": "lugares de castración",

        # Cuidados
        "cuidados": "cuidados pre y post operatorios",
        "preoperatorio": "cuidados pre y post operatorios",
        "pre operatorio": "cuidados pre y post operatorios",
        "antes": "cuidados pre y post operatorios",
        "ayuno": "cuidados pre y post operatorios",
        "preparación": "cuidados pre y post operatorios",
        "postoperatorio": "cuidados pre y post operatorios",
        "post operatorio": "cuidados pre y post operatorios",
        "después": "cuidados pre y post operatorios",
        "despues": "cuidados pre y post operatorios",
        "curación": "cuidados pre y post operatorios",

        # Beneficios
        "ventajas": "ventajas de la castración",
        "beneficios": "ventajas de la castración",
        "por qué": "ventajas de la castración",
        "porque": "ventajas de la castración",

        # Edad
        "edad": "edad recomendada",
        "meses": "edad recomendada",
        "a qué edad": "edad recomendada",
        "a que edad": "edad recomendada",

        # Procedimiento
        "procedimiento": "procedimiento de castración",
        "cómo": "procedimiento de castración",
        "como": "procedimiento de castración",
        "qué hacen": "procedimiento de castración",
        "que hacen": "procedimiento de castración",
        "operan": "procedimiento de castración",
        "operación": "procedimiento de castración",

        # Especies
        "especie": "especies que se castran",
        "animal": "especies que se castran",
        "perro": "especies que se castran",
        "gato": "especies que se castran",

        # Cantidad
        "cuántos": "cantidad diaria de castraciones",
        "cuantos": "cantidad diaria de castraciones",
        "cantidad": "cantidad diaria de castraciones",

        # Turnos
        "turno": "orden de llegada",
        "orden": "orden de llegada"
    }

    # --- Buscar coincidencias exactas ---
    for clave, tema in claves.items():
        if clave in pregunta:
            inicio = info_local.find(tema.lower())
            if inicio != -1:
                fin = info_local.find("\n\n", inicio)
                if fin == -1:
                    fin = len(info_local)
                return info_local[inicio:fin].strip().capitalize()

    # --- Buscar coincidencias difusas ---
    posibles = list(claves.keys())
    match = difflib.get_close_matches(pregunta, posibles, n=1, cutoff=0.6)
    if match:
        tema = claves[match[0]]
        inicio = info_local.find(tema.lower())
        if inicio != -1:
            fin = info_local.find("\n\n", inicio)
            if fin == -1:
                fin = len(info_local)
            return info_local[inicio:fin].strip().capitalize()

    # --- Si no encontró nada ---
    guardar_pregunta_no_respondida(pregunta)
    return "Lo siento, no tengo información sobre ese tema. Podés preguntar por horarios, lugares o cuidados de castración."

# --- MENÚ LATERAL ---
menu = st.sidebar.radio("📋 Menú", ["Chat", "Preguntas pendientes"])

# --- CHAT ---
if menu == "Chat":
    if "historial" not in st.session_state:
        st.session_state.historial = deque(maxlen=6)
        st.session_state.historial.append(
            {"role": "assistant", "content": "¡Hola! 👋 Soy Carla, asistente de Zoonosis. ¿En qué puedo ayudarte hoy?"}
        )

    pregunta = st.chat_input("Escribí tu pregunta aquí...")

    if pregunta:
        st.session_state.historial.append({"role": "user", "content": pregunta})
        respuesta = buscar_respuesta_local(pregunta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})

    for msg in st.session_state.historial:
        if msg["role"] == "user":
            st.markdown(f"🧑‍💬 **Tú:** {msg['content']}")
        else:
            st.markdown(f"🐾 **Carla:** {msg['content']}")

# --- PREGUNTAS PENDIENTES ---
elif menu == "Preguntas pendientes":
    st.header("❓ Preguntas que Carla no pudo responder")
    pendientes = cargar_preguntas_pendientes()

    if pendientes:
        st.markdown("Estas son las preguntas que los usuarios hicieron y que no están en la base de datos:")
        for p in pendientes:
            st.write("• " + p.strip())

        st.download_button(
            label="📥 Descargar preguntas pendientes",
            data="".join(pendientes),
            file_name="preguntas_no_respondidas.txt",
            mime="text/plain"
        )
    else:
        st.success("✅ No hay preguntas pendientes. ¡Carla está bien informada!")
