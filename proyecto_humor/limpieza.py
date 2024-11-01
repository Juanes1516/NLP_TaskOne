import pandas as pd



"""
# Ruta al archivo CSV
csv_path = "chistes_spanish_jokes_annotated.csv"

# Cargar el CSV
df = pd.read_csv(csv_path)

# Eliminar filas duplicadas basadas en la columna 'text'
df = df.drop_duplicates(subset="text", keep="first")

# Guardar el DataFrame limpio en el mismo archivo CSV
df.to_csv(csv_path, index=False)
print(f"Archivo CSV actualizado y guardado sin duplicados como '{csv_path}'")
"""


#Limpieza de Chistes generados por IA 

csv_path2 = "chistes_combinados.csv"
# Cargar el CSV
df2 = pd.read_csv(csv_path2)

print(df2.head())

print(df2.size)

df2 = df2.drop_duplicates()

print(df2.size)

# Guardar el DataFrame limpio en el mismo archivo CSV
df2.to_csv(csv_path2, index=False)