import os
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import pytesseract
import cv2
import pytesseract

# Función para extraer fotogramas clave del video
def extract_keyframes(video_path, frame_interval=30, output_folder='frames/'):
    # Verificar si el video existe
    if not os.path.exists(video_path):
        print(f"Error: el archivo de video {video_path} no existe.")
        return []

    # Crear la carpeta de salida si no existe
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

        # Guardar fotograma cada 'frame_interval' segundos
        if frame_count % frame_interval == 0:
            frame_path = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            print(f"Fotograma guardado en: {frame_path}")

        frame_count += 1

    cap.release()
    
    if not extracted_frames:
        print("No se guardaron fotogramas. Verifica la configuración del intervalo o el video.")
    return extracted_frames

# Extraer fotogramas del video descargado
frames = extract_keyframes("85Chistes.mp4", frame_interval=60)  # Extraer fotograma cada 60 frames

# Verificar si la lista tiene fotogramas
if frames:
    print(f"Se extrajeron {len(frames)} fotogramas.")
else:
    print("No se extrajeron fotogramas.")


# Extraer fotogramas del video descargado
frames = extract_keyframes("85Chistes.mp4", frame_interval=60)  # Extraer fotograma cada 60 frames


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

# Función para extraer texto de los fotogramas usando OCR
def extract_text_from_frame(frame_path):
    img = cv2.imread(frame_path)
    text = pytesseract.image_to_string(img)

print(frames)
# Procesar cada fotograma: generar caption y extraer texto
for frame in frames:
    print("hola")
    caption = generate_caption(frame)
    text = extract_text_from_frame(frame)
    
    # Imprimir los resultados para cada fotograma
    print(f"Descripción del fotograma {frame}: {caption}")
    print(f"Texto extraído del fotograma {frame}: {text}")
