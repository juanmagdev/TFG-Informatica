import matplotlib.pyplot as plt
from brokenaxes import brokenaxes

# Datos de ejemplo 
# 1205    518.889
# 1224    243.963
# 1472    668.073
# 1743    621.568

# PARA 4 USUARIOS
iteraciones = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36,40, 44, 48, 52]
modelo_A = [292.91, 216.41, 136.07, 115.14, 95.25, 86.74, 70.15, 66.49, 52.17, 50.31, 47.82, 46.01, 45.05, 42.11, 41.48, 40.74, 40.44, 40.52, 41.21, 40.12]  # Valores del modelo A para cada iteración
time_A = [40.22, 113.13, 179.73, 217.95, 278.84, 343.22, 465.08, 607.38, 722.07, 838.86, 973.24, 1110.72, 1244.65, 1469.41, 1716.16, 2171.66, 11420.53, 12267.26, 12584.78, 13541.06]
modelo_B = [64.19, 59.23, 55.44, 55, 52.97, 50.26, 47.16, 45.42, 44.29, 43.03, 41.83, 41.25, 40.58, 39.95, 39.37, 39.01, 38.58, 38.5, 38.4, 38.28]  # Valores del modelo B para cada iteración
time_B = [40.33, 123.81, 163.87, 218.26, 283.43, 349.10, 480.23, 614.51, 728.58, 851.80, 975.62, 1122.56, 1239.18, 1487.67, 1734.89, 2045.01, 11434.92, 12092.31, 13092.02, 13513.67]
cota_superior = 260
cota_inferior = 0  # Cota inferior para cada iteración
aprox = 64.19
additional_info = 'Usuarios    Consumo\n   1205       518.889\n   1224       243.963\n   1472       668.073\n   1743       621.568'

# PARA 6 USUARIOS
# iteraciones = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28]
# modelo_A = [248.93, 217.35, 104.03, 71.97, 57.84, 31.86, 26.26, 21.97, 17.44, 16.76, 13.96, 9.65, 8.68]  # Valores del modelo A para cada iteración
# time_A = [239.80, 961.35, 2503.77, 4025.33, 5508.86, 7649.50, 9177.80, 10566.94, 12971.64, 14439.55, 15982.51, 19551.32, 21376.48]
# modelo_B = [32.74, 20.71, 19.82, 20.24, 20.25, 21.6, 20.26, 18.42, 16.83, 16.83, 16.1, 14.328, 11.61]  # Valores del modelo B para cada iteración
# time_B = [241.41, 924.73, 2471.35, 4047.40, 5582.50, 7698.55, 9226.87, 10402.91, 12775.16, 14389.89, 16033.04, 19618.98, 21488.34]
# cota_inferior = 0  # Cota inferior para cada iteración
# cota_superior = 178.52
# aprox = 32.74


# pasa time_A y time_B a minutos
time_A = [t/60 for t in time_A]
time_B = [t/60 for t in time_B]


# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(8, 5))

# Graficar Modelo A
ax.plot(time_A, modelo_A, label='SLSQP', marker='o', linestyle='-', color='blue')
# Graficar Modelo B
ax.plot(time_B, modelo_B, label='SLSQP Inicializado', marker='o', linestyle='-', color='green')

# Añadir líneas horizontales para las cotas y la región de factibilidad
ax.axhline(y=cota_inferior, color='red', linestyle='--', label='Cota Inferior')
ax.axhline(y=cota_superior, color='red', linestyle='--', label='Cota Superior') 
ax.axhline(y=aprox, color='yellow', linestyle='-', label='Método de aproximación') 

# Añadir región de factibilidad
ax.fill_betweenx([cota_inferior, cota_superior], 0, 60, color='gray', alpha=0.3, label='Región de Factibilidad')

# Añadir título y etiquetas
ax.set_title('Desempeño de SLSQP y SLSQP Inicializado en Función del Tiempo')
ax.set_xlabel('Tiempo (minutos)')
ax.set_ylabel('Vertido (kWh)')

# Ajustar los límites del eje x para enfocar solo hasta el minuto 60
ax.set_xlim([0, 60])

# Añadir leyenda
ax.legend()
ax.grid(True)

# Guardar la gráfica en un archivo de alta calidad
plt.text(0.1, 0.7, additional_info, transform=plt.gca().transAxes, fontsize=11,
         bbox=dict(facecolor='white', alpha=0.7))
plt.savefig('desempeno_modelos1.pdf', bbox_inches='tight')



# # GRAFICA ITERACIONES

# # Graficar las series con líneas
# plt.plot(iteraciones, modelo_A, 'r-', label='SLSQP')
# plt.plot(iteraciones, modelo_B, 'b-', label='SLSQP Inicializado')
# # iteraciones.append(60)
# plt.fill_between(iteraciones, cota_inferior, cota_superior, color='gray', alpha=0.3, label='Región factibilidad')
# # elimina el 60
# # iteraciones.pop()
# # Añadir puntos en las líneas para destacar
# plt.scatter(iteraciones, modelo_A, color='r', s=20, label='Puntos SLSQP')
# plt.scatter(iteraciones, modelo_B, color='b', s=20, label='Puntos SLSQP Inicializado')

# # Añadir líneas horizontales para las cotas y la región de factibilidad
# ax = plt.gca()  # Obtener el eje actual
# ax.axhline(y=cota_inferior, color='red', linestyle='--', label='Cota Inferior')
# ax.axhline(y=cota_superior, color='orange', linestyle='--', label='Cota Superior')
# ax.axhline(y=aprox, color='yellow', linestyle='-', label='Método de aproximación')
# # ax.set_xlim([0, 60])

# # Personalizar la gráfica
# plt.xlabel('Iteraciones')
# plt.ylabel('Vertido (kWh)')
# plt.title('Comparación entre SLSQP y SLSQP inicializado en función de iteraciones')
# plt.legend()
# plt.grid(True)
# plt.text(0.1, 0.7, additional_info, transform=plt.gca().transAxes, fontsize=11,
#          bbox=dict(facecolor='white', alpha=0.7))

# # Guardar la gráfica en un archivo de alta calidad
# plt.savefig('comparacion_modelos1.pdf', bbox_inches='tight')



