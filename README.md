Carla — Asistente Virtual de Zoonosis

Proyecto desarrollado en el marco de Práctica Profesionalizante III (PP3) – Tecnicatura en Ciencia de Datos e Inteligencia Artificial.

Carla es un chatbot creado para asistir a la comunidad de Termas de Río Hondo (Santiago del Estero, Argentina), brindando información clara y accesible sobre los servicios del Centro Municipal de Salud y Zoonosis Animal: castración, vacunación antirrábica, cuidados pre y post operatorios, adopciones y asistencia en casos de animales encontrados.

El proyecto surge del diagnóstico institucional donde se identificaron problemas como:

Falta de información clara para la comunidad

Comunicación limitada sobre horarios y lugares

Desconocimiento de campañas gratuitas

Dificultad para acceder a información confiable

Carla se propone como una solución digital accesible, automatizada y de rápido acceso, que mejora la comunicación entre municipio y vecinos.

Objetivos del Proyecto
Objetivo general

Desarrollar una herramienta digital basada en datos que mejore la comunicación del municipio, brindando información inmediata y organizada sobre servicios de Zoonosis.

Objetivos específicos

Brindar información confiable sobre castraciones, horarios, lugares y cuidados.

Implementar una base de conocimiento editable y escalable.

Incorporar comprensión semántica para responder preguntas variadas.

Registrar métricas de uso para análisis posteriores.

Integrar un flujo de datos ciudadano mediante Google Forms, Sheets y Looker Studio.

Vincular el chatbot con las necesidades reales detectadas en el diagnóstico comunitario.

Relevamiento ciudadano mediante Google Forms

Para fundamentar el proyecto y entender las necesidades reales de la comunidad, se desarrolló el formulario:

 “Castración Gratuita — Diagnóstico Ciudadano”

Recopiló información sobre:

 1. Conocimiento del servicio

Si sabían que la castración era gratuita

Si conocían los puntos de atención
➡ Se detectó falta significativa de información oficial

 2. Participación previa en campañas

Si participaron en años anteriores
➡ Mayoría sin participación → necesidad de canales más claros

 3. Horarios y días preferidos

Disponibilidad ciudadana
➡ Determinó ajustes sugeridos para operativos futuros

 4. Motivos de no participación

Transporte

Desconocimiento

Horarios poco convenientes

Temor al procedimiento
➡ El principal obstáculo es la falta de información clara

 5. Nivel de satisfacción

Valoración del servicio
➡ Alto nivel de satisfacción → el problema es informativo, no de calidad

ntegración con Google Sheets y Looker Studio

Toda la información del formulario se almacena automáticamente en Google Sheets, lo que permitió:

Consolidar respuestas ciudadanas

Integrar datos históricos (2019–2025)

Normalizar barrios y motivos de participación

Crear un tablero digital con:

✔ Castraciones por barrio
✔ Tendencia histórica
✔ Conocimiento del servicio
✔ Satisfacción
✔ Participación ciudadana
✔ Motivos de no participación
✔ Preferencias horarias

Relación entre el formulario y el chatbot

El relevamiento ciudadano fue clave para:

✔ Construir la base de conocimiento

La información de castración, vacunación, adoptores, cuidados y horarios proviene de los resultados analizados en los formularios.

✔ Identificar temas prioritarios

Se detectó que la ciudadanía necesita:

Horarios claros

Indicaciones pre y post operatorias

Detalles del procedimiento

Información sobre animales encontrados

Respuestas rápidas

✔ Justificar la necesidad de Carla

Los datos confirmaron la ausencia de un canal digital unificado, lo cual motivó la creación de un chatbot accesible desde cualquier dispositivo.

✔ Mejorar el contenido del chatbot

Los temas más consultados se convirtieron en categorías principales del archivo info_zoonosis.txt.

Descripción técnica del chatbot

Carla combina coincidencia de palabras clave y comprensión semántica aplicada mediante:

TF-IDF vectorization

Cosine similarity

Esto permite reconocer preguntas similares aunque el usuario no use las mismas palabras.

Ejemplo:

“¿A qué hora castran?”

“¿Cuál es el horario de castración?”

Ambas llevan a la misma respuesta.

Tecnologías utilizadas:

Tecnología       /           Herramienta	Uso
Python 3.11	              Desarrollo principal
Streamlit	               Interfaz web del chatbot
scikit-learn	            TF-IDF + Cosine Similarity
Matplotlib	              Visualización de estadísticas
Archivos .txt/.log	      Base de conocimiento y registros
Google Forms	            Relevamiento ciudadano inicial
Google Sheets	            Almacenamiento centralizado

ase de conocimiento

La información que Carla utiliza está almacenada en:

info_zoonosis.txt

Incluye contenido sobre:

Horarios y lugares de castración

Procedimiento quirúrgico

Edad y preparación del animal

Cuidados pre y post operatorios

Vacunación y desparasitación

Adopciones

Animales encontrados

El archivo es editable desde el Modo Administrador.

Próxima etapa: migración a base de datos SQL (SQLite o MySQL).

Panel de estadísticas

La aplicación almacena métricas en tiempo real:

Total de preguntas

Preguntas respondidas

Preguntas no respondidas

Efectividad del chatbot

Historial de uso

Estos datos se visualizan con Matplotlib desde la app.

Archivos generados automáticamente:
estadisticas.log
preguntas_no_respondidas.log

Modo Administrador

Permite:

Editar toda la información usada por el chatbot

Actualizar textos y agregar nuevos temas

Gestionar contenido sin modificar el código

Instalación y ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>

2️⃣ Instalar dependencias
pip install -r requirements.txt

3️⃣ Ejecutar Carla
streamlit run app.py


Futuras mejoras

✔ Integración con SQLite/MySQL

✔ Análisis semántico más profundo

✔ Respuestas generadas con modelos de IA (GPT / LLM local)

✔ Registro de turnos en Excel / Sheets

✔ Dashboard integrado dentro del chatbot

✔ Estadísticas avanzadas:

consultas por día

palabras más frecuentes

tasa de efectividad

✔ Versión móvil / PWA

Créditos

Desarrollado por Corbalan Octavio, Gonzalez Carla, Medinas Kevin, Soria Cristian, Cajal Milagros y Correa Emmanuel.
Tecnicatura en Ciencia de Datos e Inteligencia Artificial
Práctica Profesionalizante III — 2025
Termas de Río Hondo, SDE
