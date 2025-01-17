import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import Button

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

# Crear una copia explícita del DataFrame
filtered_data = analyze_dataset[numerical_columns].copy()

# Winsorizing (recortar valores extremos)
for column in numerical_columns:
    filtered_data.loc[:, column] = filtered_data[column].clip(
        lower=filtered_data[column].quantile(0.01),
        upper=filtered_data[column].quantile(0.99)
    )

# Manejar valores faltantes: eliminar filas con NaN
filtered_data = filtered_data.dropna()

# Verificar el resumen estadístico de las columnas numéricas
print(filtered_data.describe())

# Configurar el estilo global
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

class GraphManager:
    def __init__(self, data):
        self.data = data
        self.current_index = 0
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111)
        
        # Lista de títulos para mostrar progreso
        self.titles = [
            'Matriz de Correlación',
            'Boxplots',
            'ABV vs Densidad Original',
            'IBU vs Color',
            'Distribución ABV',
            'Distribución IBU'
        ]
        
    def plot_current(self):
        self.ax.clear()
        if self.current_index == 0:
            sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f', ax=self.ax)
            self.ax.set_title('Matriz de Correlación de Variables', pad=20)
            
        elif self.current_index == 1:
            sns.boxplot(data=self.data, ax=self.ax)
            self.ax.set_title('Distribución y Outliers por Variable', pad=20)
            plt.xticks(rotation=45)
            
        elif self.current_index == 2:
            sns.scatterplot(data=self.data, x='og', y='abv', alpha=0.5, ax=self.ax)
            self.ax.set_title('Relación entre ABV y Densidad Original', pad=20)
            self.ax.set_xlabel('Densidad Original (OG)')
            self.ax.set_ylabel('Alcohol por Volumen (ABV)')
            
        elif self.current_index == 3:
            sns.scatterplot(data=self.data, x='color', y='ibu', alpha=0.5, ax=self.ax)
            self.ax.set_title('Relación entre IBU y Color', pad=20)
            self.ax.set_xlabel('Color (SRM)')
            self.ax.set_ylabel('Amargor (IBU)')
            
        elif self.current_index == 4:
            sns.histplot(data=self.data, x='abv', kde=True, color='skyblue', ax=self.ax)
            self.ax.axvline(self.data['abv'].mean(), color='red', linestyle='dashed',
                          label=f'Media: {self.data["abv"].mean():.1f}%')
            self.ax.axvline(self.data['abv'].median(), color='blue', linestyle='dashed',
                          label=f'Mediana: {self.data["abv"].median():.1f}%')
            self.ax.set_title('Distribución del Contenido Alcohólico (ABV)', pad=20)
            self.ax.set_xlabel('Alcohol por Volumen (%)')
            self.ax.set_ylabel('Frecuencia')
            self.ax.legend()
            
        else:  # self.current_index == 5
            sns.histplot(data=self.data, x='ibu', kde=True, color='lightgreen', ax=self.ax)
            self.ax.axvline(self.data['ibu'].mean(), color='red', linestyle='dashed',
                          label=f'Media: {self.data["ibu"].mean():.1f}')
            self.ax.axvline(self.data['ibu'].median(), color='blue', linestyle='dashed',
                          label=f'Mediana: {self.data["ibu"].median():.1f}')
            self.ax.set_title('Distribución del Amargor (IBU)', pad=20)
            self.ax.set_xlabel('International Bitterness Units')
            self.ax.set_ylabel('Frecuencia')
            self.ax.legend()
            
        # Mostrar progreso actual
        plt.figtext(0.5, 0.02, f'Gráfico {self.current_index + 1} de 6: {self.titles[self.current_index]}',
                   ha='center', va='center')
        self.fig.canvas.draw_idle()
        
    def next_plot(self, event):
        self.current_index = (self.current_index + 1) % 6
        self.plot_current()
        
    def prev_plot(self, event):
        self.current_index = (self.current_index - 1) % 6
        self.plot_current()
        
    def show_plots(self):
        # Crear botones
        ax_prev = plt.axes([0.25, 0.05, 0.1, 0.04])
        ax_next = plt.axes([0.65, 0.05, 0.1, 0.04])
        btn_next = Button(ax_next, 'Siguiente')
        btn_prev = Button(ax_prev, 'Anterior')
        
        # Conectar eventos
        btn_next.on_clicked(self.next_plot)
        btn_prev.on_clicked(self.prev_plot)
        
        # Mostrar primer gráfico
        self.plot_current()
        plt.show()

# Crear y mostrar los gráficos
graph_manager = GraphManager(filtered_data)
graph_manager.show_plots()

