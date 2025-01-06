import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
analyze_dataset = pd.read_csv(
    r"C:\Users\lucas\Desktop\Programacion\Programacion_Cervecerias\Analisis Hombrew\Analisis-de-Homebrew-Recipes\data\recipes_full.txt",
    delimiter=',',
    header=None, on_bad_lines="skip", # Ignorar encabezados existentes
    low_memory=False
)

# Seleccionar solo las primeras 11 columnas si son las relevantes
analyze_dataset = analyze_dataset.iloc[:, :11]

# Asignar nombres a las columnas
analyze_dataset.columns = ['name', 'url', 'method', 'style', 'batch', 'og', 'fg', 'abv', 'ibu', 'color', 'extra']

# Seleccionar columnas numéricas
numerical_columns = ['og', 'fg', 'abv', 'ibu', 'color']
filtered_data = analyze_dataset[numerical_columns]

# Verificar tipos de datos
print("Tipos de datos antes de la conversión:")
print(filtered_data.dtypes)

# Convertir columnas a numéricas
for column in numerical_columns:
    filtered_data[column] = pd.to_numeric(filtered_data[column], errors='coerce')

# Manejar valores faltantes
filtered_data.dropna(subset=numerical_columns, inplace=True)

# Verificar tipos de datos después de la conversión
print("Tipos de datos después de la conversión:")
print(filtered_data.dtypes)

# Graficar
filtered_data.hist(figsize=(10, 8))
plt.tight_layout()
plt.show()
