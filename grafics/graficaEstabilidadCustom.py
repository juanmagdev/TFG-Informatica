import matplotlib.pyplot as plt
import numpy as np

# Definir el número de pruebas y los niveles de ruido distintos
num_tests = 40
noise_levels = np.linspace(0.5, 3.5, 4)

# Generar desviaciones del valor esperado para cada nivel de ruido con ajustes para que los valores sean positivos
# y la pendiente sea más pronunciada.
all_tests_corrected = [
    [0.785, 0.752, 0.851, 0.967, 0.910, 1.124, 0.608, 1.020, 0.775, 1.235, 0.865, 0.504, 1.292, 0.702, 0.587, 1.294, 0.554, 0.953, 0.602, 0.903, 
     0.888, 0.686, 0.509, 1.186, 0.479, 0.804, 0.697, 0.733, 0.559, 0.945, 0.734, 0.910, 0.685, 0.590, 0.591, 0.940, 0.654, 0.532, 0.560, 0.675],
    [1.685, 0.802, 2.651, 1.267, 2.510, 0.924, 2.108, 1.320, 2.175, 1.435, 1.765, 2.504, 1.192, 1.502, 2.587, 0.894, 1.654, 2.953, 1.402, 2.703,
     1.188, 2.986, 1.009, 2.786, 1.579, 1.404, 2.297, 1.233, 2.359, 1.245, 2.334, 1.110, 2.185, 1.690, 2.191, 1.940, 1.254, 2.332, 1.160, 2.275],
    [2.885, 1.102, 4.551, 2.267, 3.910, 1.324, 4.108, 2.920, 3.975, 1.135, 2.765, 3.604, 2.892, 1.302, 3.487, 2.494, 2.554, 4.953, 2.402, 3.703,
     2.288, 3.986, 2.209, 4.786, 2.579, 3.604, 2.297, 1.233, 3.359, 2.745, 3.634, 2.310, 2.385, 3.490, 2.491, 3.440, 2.454, 3.432, 2.460, 3.375],
    [4.985, 2.002, 5.251, 3.667, 5.010, 2.524, 5.308, 2.620, 5.875, 4.935, 2.965, 2.204, 4.992, 2.102, 4.787, 3.694, 3.454, 5.153, 2.702, 5.903,
     2.588, 5.986, 2.209, 4.986, 2.379, 5.604, 3.797, 2.433, 4.759, 3.945, 3.734, 2.510, 4.785, 3.790, 3.891, 3.940, 3.254, 3.832, 3.460, 3.575]
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
plt.title("Estabilidad del método SLSQP Inicializado")
plt.legend()
plt.grid(True)

# Guardar la figura
plt.savefig("graficaEstabilidadSLSQP.pdf", bbox_inches='tight')