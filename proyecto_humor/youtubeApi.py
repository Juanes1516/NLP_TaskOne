import os
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import pytesseract

"""
# Función para descargar un video de YouTube
def download_video_from_youtube(video_url, output_path="video.mp4"):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    print(f"Descargando: {yt.title}")
    stream.download(filename=output_path)
    print(f"Video descargado en {output_path}")

# URL del video de YouTube
id = 'PzluiBkGZGk'
video_url = f'https://www.youtube.com/watch?v=PzluiBkGZGk'  # Reemplaza con la URL del video
download_video_from_youtube(video_url)
"""
import cv2

# Función para extraer fotogramas clave del video
def extract_keyframes(video_path, frame_interval=30, output_folder='frames/'):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success = True
    extracted_frames = []

    while success:
        success, frame = cap.read()
        if not success:
            break

        # Guardar fotograma cada 'frame_interval' segundos
        if frame_count % frame_interval == 0:
            frame_path = f"{output_folder}frame_{frame_count}.jpg"
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            print(f"Fotograma guardado en: {frame_path}")

        frame_count += 1

    cap.release()
    return extracted_frames

# Extraer fotogramas del video descargado
frames = extract_keyframes("85Chistes.mp4", frame_interval=60)  # Extraer fotograma cada 60 frames

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Cargar el modelo BLIP de Hugging Face
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Función para generar descripciones automáticas
def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

"""# Generar descripciones para cada fotograma
for frame in frames:
    caption = generate_caption(frame)
    print(f"Descripción del fotograma {frame}: {caption}")
    break"""


import pytesseract

# Función para extraer texto de los fotogramas usando OCR
def extract_text_from_frame(frame_path):
    img = cv2.imread(frame_path)
    text = pytesseract.image_to_string(img)
    return text

"""
# Extraer texto de los fotogramas
for frame in frames:
    text = extract_text_from_frame(frame)
    print(f"Texto extraído del fotograma {frame}: {text}")
"""



# Procesar cada fotograma: generar caption y extraer texto
for frame in frames:
    caption = generate_caption(frame)
    text = extract_text_from_frame(frame)
    
    # Imprimir los resultados para cada fotograma
    print(f"Descripción del fotograma {frame}: {caption}")
    print(f"Texto extraído del fotograma {frame}: {text}")
