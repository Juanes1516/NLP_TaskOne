import pandas as pd

# Cargar el CSV original y el nuevo CSV con chistes generados
csv_original = "chistes_spanish_jokes_annotated.csv"
csv_nuevo = "chistes_generados.csv"

# Leer ambos archivos CSV
df_original = pd.read_csv(csv_original)
df_nuevo = pd.read_csv(csv_nuevo)

# Verificar y añadir las columnas faltantes en el nuevo DataFrame para que coincidan con el formato original
columnas_originales = ["text", "evaluacion_1", "evaluacion_2", "evaluacion_3", "evaluacion_4", "tipo_origen", "fuente"]

# Renombrar la columna 'chiste' del nuevo CSV a 'text' y agregar las columnas faltantes
df_nuevo = df_nuevo.rename(columns={"chiste": "text"})
for columna in columnas_originales:
    if columna not in df_nuevo.columns:
        # Añadir columnas con valores por defecto según el tipo de información
        if columna == "tipo_origen":
            df_nuevo[columna] = "IA-generado"
        elif columna == "fuente":
            df_nuevo[columna] = "OpenAI GPT"
        else:
            df_nuevo[columna] = None  # Llena las evaluaciones con valores vacíos

# Concatenar el DataFrame original con el nuevo
df_combinado = pd.concat([df_original, df_nuevo], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
df_combinado.to_csv("chistes_combinados.csv", index=False)
print("El archivo 'chistes_combinados.csv' ha sido creado con los datos de ambos CSVs.")
