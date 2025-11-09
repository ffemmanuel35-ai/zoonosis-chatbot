# 🐾 Chatbot "Carla" usando Hugging Face - Blenderbot
# Modelo: facebook/blenderbot-400M-distill

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

print("🐾 Iniciando Carla...")

# Intentar cargar modelo y tokenizer desde Hugging Face
try:
    model_name = "facebook/blenderbot-400M-distill"
    tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    print("✅ Modelo cargado correctamente desde Hugging Face.")
except Exception as e:
    print(f"⚠️ Error al conectar con Hugging Face: {e}")
    exit()

# 💬 Función para conversar
def chat_with_carla():
    print("\n🐾 Carla: ¡Hola! Soy tu asistente virtual. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("🐾 Carla: ¡Hasta luego! 🐕")
            break

        try:
            inputs = tokenizer([user_input], return_tensors="pt")
            reply_ids = model.generate(**inputs)
            reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
            print(f"🐾 Carla: {reply}\n")
        except Exception as e:
            print(f"⚠️ Ocurrió un error procesando tu mensaje: {e}\n")

# 🚀 Iniciar el chat
if __name__ == "__main__":
    chat_with_carla()
