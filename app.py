import streamlit as st
from collections import deque
import difflib
import datetime
import os
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

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

# --- CONFIGURACIÓN ---
ADMIN_PASSWORD = "1234"
STATS_FILE = "estadisticas.log"

# --- FUNCIONES AUXILIARES ---
def cargar_info():
    try:
        with open("info_zoonosis.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ No se encontró el archivo de información local."

def guardar_info(texto):
    with open("info_zoonosis.txt", "w", encoding="utf-8") as f:
        f.write(texto)

def guardar_pregunta_no_respondida(pregunta):
    with open("preguntas_no_respondidas.log", "a", encoding="utf-8") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] {pregunta}\n")
    registrar_estadistica("no_respondidas")

def cargar_preguntas_pendientes():
    if not os.path.exists("preguntas_no_respondidas.log"):
        return []
    with open("preguntas_no_respondidas.log", "r", encoding="utf-8") as f:
        return f.readlines()

def registrar_estadistica(tipo):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(STATS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{fecha},{tipo}\n")

def obtener_estadisticas():
    if not os.path.exists(STATS_FILE):
        return {"total": 0, "no_respondidas": 0}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    total = len(lineas)
    no_respondidas = sum(1 for l in lineas if "no_respondidas" in l)
    return {"total": total, "no_respondidas": no_respondidas}

# --- CARGAR INFORMACIÓN LOCAL ---
info_local = cargar_info().lower()

# --- FUNCIÓN DE BÚSQUEDA SEMÁNTICA ---
def similitud_semantica(pregunta, claves):
    corpus = list(claves.keys()) + [pregunta]
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    similitudes = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
    mejor_indice = np.argmax(similitudes)
    if similitudes[mejor_indice] > 0.3:  # umbral de similitud
        return list(claves.keys())[mejor_indice]
    return None

# --- FUNCIÓN: BUSCAR RESPUESTA LOCAL ---
def buscar_respuesta_local(pregunta):
    pregunta = pregunta.lower()

    animales_prohibidos = ["conejo", "hurón", "hamster", "loro", "cobayo", "ave", "pájaro", "tortuga"]
    for animal in animales_prohibidos:
        if animal in pregunta:
            registrar_estadistica("respondida")
            return random.choice([
                "❌ Solo se castran perros y gatos en el área de Zoonosis.",
                "🚫 En Zoonosis solo se atienden perros y gatos, no otras especies."
            ])

    claves = {
        "horario": "horario de castración",
        "hora": "horario de castración",
        "mañana": "horario de castración",
        "cuando": "horario de castración",
        "día": "horario de castración",
        "dias": "horario de castración",
        "lugar": "lugares de castración",
        "dónde": "lugares de castración",
        "donde": "lugares de castración",
        "direccion": "lugares de castración",
        "hospital": "lugares de castración",
        "barrio": "lugares de castración",
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
        "ventajas": "ventajas de la castración",
        "beneficios": "ventajas de la castración",
        "por qué": "ventajas de la castración",
        "porque": "ventajas de la castración",
        "edad": "edad recomendada",
        "meses": "edad recomendada",
        "a qué edad": "edad recomendada",
        "a que edad": "edad recomendada",
        "procedimiento": "procedimiento de castración",
        "cómo": "procedimiento de castración",
        "como": "procedimiento de castración",
        "qué hacen": "procedimiento de castración",
        "que hacen": "procedimiento de castración",
        "operan": "procedimiento de castración",
        "operación": "procedimiento de castración",
        "especie": "especies que se castran",
        "animal": "especies que se castran",
        "perro": "especies que se castran",
        "gato": "especies que se castran",
        "cuántos": "cantidad diaria de castraciones",
        "cuantos": "cantidad diaria de castraciones",
        "cantidad": "cantidad diaria de castraciones",
        "turno": "orden de llegada",
        "orden": "orden de llegada"
    }

    # --- coincidencia exacta ---
    for clave, tema in claves.items():
        if clave in pregunta:
            registrar_estadistica("respondida")
            inicio = info_local.find(tema.lower())
            if inicio != -1:
                fin = info_local.find("\n\n", inicio)
                if fin == -1:
                    fin = len(info_local)
                respuesta = info_local[inicio:fin].strip().capitalize()
                return random.choice([
                    respuesta,
                    f"Claro 😊 {respuesta}",
                    f"Por supuesto 🐶 {respuesta}",
                    f"¡Buena pregunta! 🐾 {respuesta}"
                ])

    # --- similitud semántica (mejorada) ---
    match_sem = similitud_semantica(pregunta, claves)
    if match_sem:
        registrar_estadistica("respondida")
        tema = claves[match_sem]
        inicio = info_local.find(tema.lower())
        if inicio != -1:
            fin = info_local.find("\n\n", inicio)
            if fin == -1:
                fin = len(info_local)
            respuesta = info_local[inicio:fin].strip().capitalize()
            return f"Creo que te referís a esto 🐾:\n\n{respuesta}"
        
        # 💾 Guardar preguntas sin respuesta (en dos formatos)
    with open("preguntas_no_resueltas.txt", "a", encoding="utf-8") as f:
        f.write(pregunta + "\n")

    guardar_pregunta_no_respondida(pregunta)
    return random.choice([
        "Lo siento 😕, no tengo información sobre eso. Podés preguntar por horarios, lugares o cuidados de castración.",
        "Mmm... no encuentro esa información 🐾. Probá preguntarme sobre horarios, cuidados o lugares.",
        "No tengo esa información todavía 😅, pero puedo contarte sobre castraciones, horarios o cuidados."
    ])

# --- RECORDATORIOS AUTOMÁTICOS ---
def mostrar_recordatorio():
    recordatorios = [
        "💉 Recordá vacunar a tus mascotas todos los años.",
        "🚶‍♂️ Usá siempre correa al sacar a pasear a tu perro.",
        "🐱 La castración también es importante para los gatos, no solo para los perros.",
        "🌡️ Si notás fiebre o decaimiento, llevá tu mascota al veterinario.",
        "🐾 Adoptar es un acto de amor 💚"
    ]
    if random.random() < 0.25:
        st.info(random.choice(recordatorios))

# --- MENÚ LATERAL ---
menu = st.sidebar.radio("📋 Menú", ["Chat", "Preguntas pendientes", "Estadísticas", "Modo administrador"])

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
        mostrar_recordatorio()

    for msg in st.session_state.historial:
        if msg["role"] == "user":
            st.markdown(f"<div style='background-color:#E3F2FD;padding:8px;border-radius:10px;margin:4px 0;'>🧑‍💬 <b>Tú:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#FFF3E0;padding:8px;border-radius:10px;margin:4px 0;'>🐾 <b>Carla:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --- PREGUNTAS PENDIENTES ---
elif menu == "Preguntas pendientes":
    st.header("❓ Preguntas que Carla no pudo responder")
    pendientes = cargar_preguntas_pendientes()
    if pendientes:
        for p in pendientes:
            st.write("• " + p.strip())
    else:
        st.success("✅ No hay preguntas pendientes. ¡Carla está bien informada!")

# --- ESTADÍSTICAS ---
elif menu == "Estadísticas":
    st.header("📊 Estadísticas de uso del chatbot")
    stats = obtener_estadisticas()
    st.write(f"**Total de interacciones:** {stats['total']}")
    st.write(f"**Preguntas sin respuesta:** {stats['no_respondidas']}")
    if stats['total'] > 0:
        porcentaje = (stats['no_respondidas'] / stats['total']) * 100
        st.write(f"**Porcentaje sin respuesta:** {porcentaje:.2f}%")

        # --- gráfico visual ---
        fig, ax = plt.subplots()
        ax.bar(["Respondidas", "No respondidas"], [stats['total'] - stats['no_respondidas'], stats['no_respondidas']])
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)

# --- MODO ADMIN ---
elif menu == "Modo administrador":
    st.header("🔒 Modo administrador")
    password = st.text_input("Ingresá la clave de administrador:", type="password")

    if password == ADMIN_PASSWORD:
        st.success("✅ Acceso concedido.")
        texto_actual = cargar_info()
        nuevo_texto = st.text_area("✏️ Editar información de Zoonosis:", value=texto_actual, height=400)
        if st.button("💾 Guardar cambios"):
            guardar_info(nuevo_texto)
            st.success("✅ Información actualizada correctamente.")
    elif password:
        st.error("❌ Clave incorrecta.")
