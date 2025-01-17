import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
analyze_dataset = pd.read_csv(
    r"C:\Users\lucas\Desktop\Programacion\Programacion_Cervecerias\Analisis Hombrew\Analisis-de-Homebrew-Recipes\data\recipes_full.txt",
    delimiter=',',
    header=None, on_bad_lines='skip',
    low_memory=False
)

# Seleccionar las primeras 11 columnas relevantes
analyze_dataset = analyze_dataset.iloc[:, :11]

# Asignar nombres a las columnas
analyze_dataset.columns = ['name', 'url', 'method', 'style', 'batch', 'og', 'fg', 'abv', 'ibu', 'color', 'extra']

# Seleccionar las columnas numéricas
numerical_columns = ['og', 'fg', 'abv', 'ibu', 'color']

# Limpieza de columnas numéricas
for column in numerical_columns:
    analyze_dataset[column] = analyze_dataset[column].astype(str)
    analyze_dataset[column] = analyze_dataset[column].str.replace('[^0-9.]', '', regex=True)
    analyze_dataset[column] = pd.to_numeric(analyze_dataset[column], errors='coerce')

# Filtrar las columnas seleccionadas
filtered_data = analyze_dataset[numerical_columns]

# Winsorizing (recortar valores extremos)
for column in numerical_columns:
    filtered_data[column] = filtered_data[column].clip(
        lower=filtered_data[column].quantile(0.01),
        upper=filtered_data[column].quantile(0.99)
    )

# Manejar valores faltantes: eliminar filas con NaN
filtered_data.dropna(inplace=True)

# Verificar el resumen estadístico de las columnas numéricas
print(filtered_data.describe())

# Crear una figura para la matriz de correlación
plt.figure(figsize=(10, 8))
sns.heatmap(filtered_data.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlación')
plt.tight_layout()
plt.show()

# Crear boxplots
plt.figure(figsize=(12, 6))
filtered_data.boxplot(column=numerical_columns)
plt.title('Distribución y Outliers por Variable')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Graficar scatter plots relevantes
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ABV vs OG
sns.scatterplot(data=filtered_data, x='og', y='abv', ax=axes[0])
axes[0].set_title('ABV vs Densidad Original')

# IBU vs Color
sns.scatterplot(data=filtered_data, x='color', y='ibu', ax=axes[1])
axes[1].set_title('IBU vs Color')

plt.tight_layout()
plt.show()

# Calcular límites automáticos para los ejes
limits = {
    column: (filtered_data[column].min(), filtered_data[column].max())
    for column in numerical_columns
}

# Graficar
if not filtered_data.empty:
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    axes = axes.flatten()

    columns = ["og", "fg", "abv", "ibu", "color"]

    for i, column in enumerate(columns):
        ax = axes[i]
        ax.hist(filtered_data[column], bins=30, alpha=0.7, color="skyblue", edgecolor="black")
        ax.axvline(filtered_data[column].mean(), color="red", linestyle="dashed", linewidth=1, label="Media")
        ax.axvline(filtered_data[column].median(), color="blue", linestyle="dashed", linewidth=1, label="Mediana")
        ax.set_title(f"Distribución de {column}")
        ax.set_xlim(limits[column])
        ax.set_xlabel(column)
        ax.set_ylabel("Frecuencia")
        ax.legend()

    if len(columns) < len(axes):
        axes[-1].axis("off")

    plt.tight_layout()
    plt.show()
else:
    print("No hay datos numéricos válidos para graficar.")

