import os
from openai import OpenAI
import pandas as pd


client = OpenAI(
    # This is the default and can be omitted
    api_key= "",
)

def generar_chistes(prompt):
    try: 
        chat_completion = client.chat.completions.create(
            model = "gpt-4",
            messages=[
              {"role": "system", "content": "Eres un asistente que ayuda a generar chistes en español."},
              {"role": "user", "content": prompt}
         ],
          max_tokens=60,        # Ajusta según tus necesidades
          temperature=0.5,      # Controla la creatividad del modelo
          frequency_penalty=0.5,  # Reduce la repetición de frases
          presence_penalty=0.8    # Aumenta la probabilidad de nuevos temas
    
        )
        
        chiste = chat_completion.choices[0].message.content.strip()
        return chiste
    except Exception as e:
        print(f"Error al generar el chiste: {e}")
        return ""
        
# Lista de prompts para generar diferentes tipos de chistes
prompts = [
    "Escribe un chiste sobre esperar en una fila larga en un banco en Latinoamérica.",
    "Crea un chiste en español que no se base en un juego de palabras.",
    "Escribe un chiste sarcástico en español sobre la vida cotidiana.",
    "Genera un chiste en español sobre problemas tecnológicos modernos.",
    "Escribe un chiste en español que sea original y diferente a los típicos juegos de palabras.",
    "Genera un chiste corto en español sobre un animal.",
    "Escribe un chiste en español usando un juego de palabras.",
    "Crea un chiste tipo pregunta-respuesta en español sobre la escuela.",
    "Haz un chiste divertido en español sobre comida.",
    "Genera un chiste en español sobre la tecnología.",
    "Genera un chiste en un contexto Colombiano",
    "Genera un chiste en un contexto Colombiano costeño"
    "Genera un chiste en un contexto Colombiano",
    "Genera un chiste en un contexto Colombiano popular",
    "Genera un chiste en un contexto Colombiano moderno",
    "Escribe un chiste muy gracioso",
    "Escribe un chiste muy muy gracioso",
    "Escribe un chiste muy muy gracioso",
    "Escribe un chiste en español sobre el tráfico en Bogotá.",
    "Genera un chiste en español sobre el clima en Colombia.",
   
]

# Número de chistes a generar
total_chistes = 2000
chistes = []

# Generar chistes en lotes
for i in range(total_chistes):
    prompt = prompts[i % len(prompts)]  # Cambia el prompt cada ciclo para variedad
    chiste = generar_chistes(prompt)
    if chiste:  # Asegúrate de que el chiste no esté vacío
        chistes.append(chiste)
    print(f"Chiste {i+1}: {chiste}")

# Guardar los chistes en un archivo CSV
df_chistes = pd.DataFrame(chistes, columns=["chiste"])
df_chistes.to_csv("chistes_generados.csv", index=False)
print("Chistes generados y guardados en 'chistes_generados.csv'")
