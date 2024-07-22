import re
import pandas as pd
import matplotlib.pyplot as plt


# Inicializamos las listas para almacenar los datos
matrix_data = []
deviations = []

# Variables temporales para las dimensiones y tiempo de ejecución actuales
current_matrix_rows = None
current_execution_time = None

# Abrimos el archivo para leerlo
with open('resultadosCustom.txt', 'r') as file:
    lines = file.readlines()

# Recorremos las líneas del archivo
for line in lines:
    # Buscamos y extraemos el número de filas de la matriz
    if 'The dimensions of the matrix are:' in line:
        current_matrix_rows = int(re.search(r'\((\d+), \d+\)', line).group(1))
    
    # Buscamos y extraemos el tiempo de ejecución
    if 'Execution time:' in line:
        current_execution_time = float(line.split(': ')[1])
        # Guardamos los datos de filas de la matriz y tiempo de ejecución juntos
        matrix_data.append((current_matrix_rows, current_execution_time))
    
    # Buscamos y extraemos los valores de las desviaciones
    if 'deviates from' in line:
        deviation_value = float(re.search(r'deviates from \d+\.\d+ by ([\d\.\-e]+) kWh', line).group(1))
        matrix_row = int(re.search(r'for (\d+) is', line).group(1))
        deviations.append((current_matrix_rows, matrix_row, deviation_value))

# Imprimimos los resultados
print("Execution Times (rows, time):", matrix_data)
print("Deviations (rows, row, value):", deviations)


# Convertimos las listas a DataFrames para manejarlas mejor
df_times = pd.DataFrame(matrix_data, columns=['rows', 'execution_time'])
df_devs = pd.DataFrame(deviations, columns=['rows', 'row', 'deviation'])

# Calculamos la media de los tiempos de ejecución por número de filas
mean_execution_times = df_times.groupby('rows').execution_time.mean().reset_index()

# Calculamos la media de las desviaciones agrupando por el número de filas
mean_deviations = df_devs.groupby('rows').deviation.mean().reset_index()

# Imprimimos los resultados
print("Average Execution Times (rows, avg_time):")
print(mean_execution_times)

print("\nAverage Deviations (rows, avg_deviation):")
print(mean_deviations)


# Datos proporcionados
additional_info = 'max_iterations = 60000\np = 0.001'
rows = [4, 6, 8, 10, 15, 20, 25, 30, 35]
execution_time = [1.468365, 1.601016, 1.845861, 2.734902, 6.719137, 144.700834, 924.025237, 1089.988659, 1221.975587]
deviation = [0.000027, 0.000022, 0.000025, 0.000034, 0.000046, 0.000049, 0.000209, 0.001578, 0.007885]
execution_time_minutes = [t / 60 for t in execution_time]

# Primera gráfica: tiempo de ejecución
plt.figure(figsize=(10, 5))
plt.plot(rows, execution_time_minutes, marker='o', linestyle='-')
plt.xlabel('Número de usuarios')
plt.ylabel('Tiempo de ejecución (minutos)')
plt.title('Tiempo de ejecución promedio vs. Número de usuarios')
plt.grid(True)
plt.xticks(rows)
plt.tight_layout()
plt.text(0.05, 0.8, additional_info, transform=plt.gca().transAxes, fontsize=12,
         bbox=dict(facecolor='white', alpha=0.7))
plt.show()

plt.savefig('graficaCustomTiempo.pdf', bbox_inches='tight')

# Segunda gráfica: desviación
plt.figure(figsize=(10, 5))
plt.plot(rows, deviation, marker='o', linestyle='-')
plt.xlabel('Número de usuarios (Rows)')
plt.ylabel('Desviación promedio')
plt.title('Desviación promedio vs. Número de usuarios')
plt.grid(True)
plt.xticks(rows)
plt.tight_layout()
plt.text(0.05, 0.8, additional_info, transform=plt.gca().transAxes, fontsize=12,
         bbox=dict(facecolor='white', alpha=0.7))
plt.show()

# guarda las figuras en pdf
plt.savefig('graficaCustomDesviacion.pdf', bbox_inches='tight')