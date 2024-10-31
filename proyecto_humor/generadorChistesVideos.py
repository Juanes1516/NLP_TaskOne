import os
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer
from PIL import Image
import pytesseract
import pandas as pd

# Cargar el modelo BLIP de Hugging Face para captions en inglés
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Cargar el modelo de traducción de inglés a español
translation_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-es")
translation_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar el CSV existente con el esquema previamente creado
csv_path = "chistes_spanish_jokes_annotated.csv"
df = pd.read_csv(csv_path)

# Función para extraer fotogramas clave del video
def extract_keyframes(video_path, frame_interval=30, output_folder='frames/'):
    if not os.path.exists(video_path):
        print(f"Error: el archivo de video {video_path} no existe.")
        return []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Carpeta creada: {output_folder}")

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success = True
    extracted_frames = []

    while success:
        success, frame = cap.read()
        if not success:
            break

        if frame_count % frame_interval == 0:
            frame_path = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            print(f"Fotograma guardado en: {frame_path}")

        frame_count += 1

    cap.release()
    return extracted_frames

# Función para generar descripciones automáticas
def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

# Función para traducir texto del inglés al español
def translate_to_spanish(text):
    inputs = translation_tokenizer(text, return_tensors="pt")
    translated = translation_model.generate(**inputs)
    spanish_text = translation_tokenizer.decode(translated[0], skip_special_tokens=True)
    return spanish_text

# Función para extraer texto de los fotogramas usando OCR
def extract_text_from_frame(frame_path):
    img = cv2.imread(frame_path)
    text = pytesseract.image_to_string(img)
    return text

# Extraer fotogramas del video
frames = extract_keyframes("85Chistes.mp4", frame_interval=60)

# Fuente detallada
fuente_detallada = """85 Chistes Graciosos y Buenos - Compilación de Chistes Cortos, Beby, 3,02 M de suscriptores, 78.995.189 visualizaciones, 1 dic 2016"""

# Procesar cada fotograma: generar caption y extraer texto
new_rows = []
for frame in frames:
    caption = generate_caption(frame)
    caption_es = translate_to_spanish(caption)
    text = extract_text_from_frame(frame)
    
    # Combinar el caption en español y el texto extraído en una sola cadena para el chiste
    chiste = f"{caption_es} {text}"
    
    # Crear una nueva fila con el chiste y otros datos
    new_row = {
        "text": chiste,
        "evaluacion_1": None,
        "evaluacion_2": None,
        "evaluacion_3": None,
        "evaluacion_4": None,  # Nueva columna para la cuarta evaluación
        "tipo_origen": "video",
        "fuente": fuente_detallada
    }
    
    # Agregar la nueva fila a la lista de nuevas filas
    new_rows.append(new_row)

# Concatenar las nuevas filas al DataFrame existente
df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

# Reordenar las columnas para colocar "evaluacion_4" junto a las otras evaluaciones
column_order = ["text", "evaluacion_1", "evaluacion_2", "evaluacion_3", "evaluacion_4", "tipo_origen", "fuente"]
df = df[column_order]

# Guardar el DataFrame actualizado en el archivo CSV
df.to_csv(csv_path, index=False)
print(f"Archivo CSV actualizado y guardado como '{csv_path}'")
