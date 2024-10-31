import pandas as pd

# Ruta al archivo CSV
csv_path = "chistes_spanish_jokes_annotated.csv"

# Cargar el CSV
df = pd.read_csv(csv_path)

# Eliminar filas duplicadas basadas en la columna 'text'
df = df.drop_duplicates(subset="text", keep="first")

# Guardar el DataFrame limpio en el mismo archivo CSV
df.to_csv(csv_path, index=False)
print(f"Archivo CSV actualizado y guardado sin duplicados como '{csv_path}'")
