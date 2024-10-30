import pandas as pd

# Cargar el dataset dado en formato parquet
df = pd.read_parquet("hf://datasets/mrm8488/CHISTES_spanish_jokes/data/train-00000-of-00001-b70fa6139e8c3f32.parquet")

# Agregar columnas para la anotación de humor y nivel de gracia en una sola columna para cada miembro
df["evaluacion_1"] = None  # Primera evaluación (0 si no es humorístico, 1-5 si es humorístico)
df["evaluacion_2"] = None  # Segunda evaluación
df["evaluacion_3"] = None  # Tercera evaluación

# Llenar las columnas de tipo de origen y fuente para todas las filas
df["tipo_origen"] = "dataset-texto"                          # Tipo de contenido: "texto"
df["fuente"] = "Hugging Face - mrm8488/CHISTES_spanish_jokes"  # Fuente específica con créditos completos

# Verificar el nuevo DataFrame
print(df.head())

# Guardar el DataFrame actualizado como archivo CSV
df.to_csv("chistes_spanish_jokes_annotated.csv", index=False)
print("Archivo CSV guardado como 'chistes_spanish_jokes_annotated.csv'")








"""
import requests

# Tu clave API de YouTube
api_key = 'AIzaSyD__6_wQxOMABA_oyICrQUPSMUam5q3tVE'

# ID del video que quieres consultar
video_id = 'PzluiBkGZGk'

# URL base de la API de YouTube
url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics&key={api_key}'

# Hacer la solicitud HTTP
response = requests.get(url)

# Procesar la respuesta
if response.status_code == 200:
    video_info = response.json()
    if 'items' in video_info and len(video_info['items']) > 0:
        video = video_info['items'][0]
        title = video['snippet']['title']
        description = video['snippet']['description']
        views = video['statistics']['viewCount']
        likes = video['statistics']['likeCount']
        print(f"Título: {title}")
        print(f"Descripción: {description}")
        print(f"Vistas: {views}")
        print(f"Likes: {likes}")
    else:
        print("El video no fue encontrado.")
else:
    print(f"Error al hacer la solicitud: {response.status_code}")


from youtube_transcript_api import YouTubeTranscriptApi

video_id = 'VIDEO_ID_AQUI'

# Obtener la transcripción (si está disponible)
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for entry in transcript:
        print(f"{entry['start']} - {entry['text']}")
except Exception as e:
    print(f"No se pudo obtener la transcripción: {e}")

"""
