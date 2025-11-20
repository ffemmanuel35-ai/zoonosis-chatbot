 Carla — Asistente Virtual de Zoonosis

Carla es un chatbot desarrollado con Python + Streamlit para asistir a los vecinos de Termas de Río Hondo (Santiago del Estero, Argentina) brindando información sobre castraciones de perros y gatos, cuidados, horarios y más.

 Características principales

 Chat interactivo: los usuarios pueden hacer preguntas en lenguaje natural.

 Comprensión semántica: usa TF-IDF y cosine similarity para entender preguntas parecidas.

 Panel de estadísticas: registra y muestra la cantidad de preguntas respondidas y no respondidas.

 Modo administrador: permite actualizar la información del archivo info_zoonosis.txt desde la interfaz.

 Recordatorios automáticos: brindan consejos sobre salud y cuidado animal.

 Registro de preguntas no respondidas: guarda las consultas que el bot no pudo contestar para mejorar con el tiempo.

 Estructura del repositorio

├── app.py                        # Código principal del chatbot

├── info_zoonosis.txt             # Base de conocimiento local con la información que usa el bot

├── preguntas_no_respondidas.log  # Registro con fecha/hora de preguntas sin respuesta

├── estadisticas.log              # Archivo donde se guardan las métricas del uso

├── requirements.txt              # Librerías necesarias para ejecutar el proyecto

├── README.md                     # Este archivo :)

└── .devcontainer/                # Configuración opcional para desarrollo en contenedores

Requisitos previos

Python 3.10 o superior

pip actualizado

Instalación y ejecución

1_Cloná el repositorio:
git clone https://github.com/<tu_usuario>/<nombre_repositorio>.git
cd <nombre_repositorio>

2_Instalá las dependencias:
pip install -r requirements.txt

3_Ejecutá la aplicación:
streamlit run app.py

4_Abrí el enlace local o público que aparece en la consola para acceder al chatbot.

Archivos importantes

info_zoonosis.txt → contiene la información que Carla usa para responder.
Podés editarla manualmente o desde el “Modo Administrador” dentro del chatbot.

preguntas_no_respondidas.log → almacena las preguntas que los usuarios hacen y que no tienen respuesta.
Te sirve para mejorar el conocimiento del bot.

estadisticas.log → guarda métricas de uso, como preguntas respondidas y no respondidas.

Créditos

Desarrollado por Clonuel como asistente virtual para el área de Zoonosis Municipal de Termas de Río Hondo, Santiago del Estero (Argentina).
Inspirado en la idea de acercar la información pública de forma accesible y moderna.

Futuras mejoras

*Integración con base de datos externa (por ejemplo SQLite, MySQL o JSON).

*Generación automática de respuestas con IA (como GPT o un modelo local)

*Integracion de registro en planilla de excel para programar castraciones.

*Estadísticas visuales más avanzadas (📅 Gráfico de cuántas consultas hay por día.💬 Palabras más frecuentes.📈 Porcentaje de respuestas exitosas vs no respondidas)
