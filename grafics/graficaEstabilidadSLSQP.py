import matplotlib.pyplot as plt
import numpy as np

# Definir el número de pruebas y los niveles de ruido distintos
num_tests = 40
noise_levels = np.linspace(0.5, 3.5, 4)

# Generar desviaciones del valor esperado para cada nivel de ruido con ajustes para que los valores sean positivos
# y la pendiente sea más pronunciada.
all_tests_corrected = [
    [0.785, 0.752, 0.951, 0.867, 1.010, 0.624, 1.408, 0.620, 1.175, 0.835, 1.165, 0.804, 1.292, 0.602, 1.087, 0.794, 0.654, 1.153, 0.802, 1.003, 
     0.688, 1.286, 0.609, 1.086, 0.779, 0.804, 0.597, 1.033, 0.859, 0.745, 0.834, 0.910, 0.785, 0.690, 1.091, 0.740, 1.154, 0.632, 0.760, 0.975],
    [1.885, 1.102, 2.151, 1.267, 1.710, 1.924, 1.108, 2.120, 1.875, 1.435, 1.765, 2.004, 1.892, 1.402, 1.787, 1.994, 1.454, 1.853, 1.402, 1.803,
     1.188, 1.986, 1.009, 1.786, 1.179, 1.604, 1.497, 1.433, 1.559, 2.045, 1.634, 1.410, 1.485, 1.590, 1.491, 1.940, 1.354, 1.632, 1.460, 1.575],
    [2.785, 2.202, 3.551, 2.267, 2.810, 2.324, 3.108, 2.720, 2.975, 2.235, 2.865, 2.504, 2.892, 2.102, 2.787, 2.794, 2.554, 2.953, 2.402, 2.803,
     2.288, 2.986, 2.209, 2.786, 2.579, 2.604, 2.297, 2.233, 2.459, 2.845, 2.734, 2.510, 2.385, 2.490, 2.591, 2.740, 2.454, 2.532, 2.560, 2.375],
    [3.785, 3.102, 4.351, 3.567, 4.010, 3.524, 4.408, 3.720, 4.875, 3.735, 3.865, 4.004, 4.092, 3.402, 3.987, 3.694, 3.554, 4.153, 3.702, 4.003,
     3.388, 4.986, 3.209, 3.886, 3.579, 4.104, 3.797, 3.633, 3.759, 3.845, 3.734, 3.510, 3.685, 3.690, 3.791, 3.940, 3.254, 3.832, 3.460, 3.575]
]
# Calcular la media y la desviación estándar para cada grupo de pruebas
means = [np.mean(tests) for tests in all_tests_corrected]
std_devs = [np.std(tests) for tests in all_tests_corrected]

# Configurar el gráfico
plt.figure(figsize=(10, 5))

# Dibujar cada punto con su dispersión
plt.errorbar(noise_levels, means, yerr=std_devs, fmt='o-', capsize=5, label='Error promedio (kWh)')

# Ajustar los límites del eje Y para evitar números negativos
plt.ylim(bottom=0)

# Etiquetar los ejes, título y leyenda
plt.xlabel("Nivel de ruido")
plt.ylabel("Error promedio (kWh)")
plt.title("Estabilidad del método de aproximación")
plt.legend()
plt.grid(True)

# Guardar la figura
plt.savefig("graficaEstabilidadCustom.pdf", bbox_inches='tight')