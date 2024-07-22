import matplotlib.pyplot as plt
from brokenaxes import brokenaxes

# Datos de ejemplo 
# 1205    518.889
# 1224    243.963
# 1472    668.073
# 1743    621.568

# PARA 10 USUARIOS
iteraciones = [1, 2, 4, 6, 8]
modelo_A = [201.74, 89.08, 93.73, 35.43, 0.33]  # Valores del modelo A para cada iteración
time_A = [692.51, 3774, 10803, 16802, 23328]
modelo_B = [13.89, 0.88, 105.8, 48.92, 4.77]  # Valores del modelo B para cada iteración
time_B = [687.56, 3857, 10684, 17012, 24076]
cota_inferior = 0  # Cota inferior para cada iteración
cota_superior = 159.67
aprox = 13.87

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
ax.fill_betweenx([cota_inferior, cota_superior], 0, 400, color='gray', alpha=0.3, label='Región de Factibilidad')

# Añadir título y etiquetas
ax.set_title('Desempeño de SLSQP y SLSQP Inicializado en Función del Tiempo')
ax.set_xlabel('Tiempo (minutos)')
ax.set_ylabel('Vertido (kWh)')

# Añadir leyenda
ax.legend()
ax.grid(True)

# Guardar la gráfica en un archivo de alta calidad
plt.savefig('desempeno_modelos3.pdf', bbox_inches='tight')



# GRAFICA ITERACIONES

# # Graficar las series con líneas
# plt.plot(iteraciones, modelo_A, 'b-', label='SLSQP')
# plt.plot(iteraciones, modelo_B, 'g-', label='SLSQP Inicializado')
# # iteraciones.append(60)
# plt.fill_between(iteraciones, cota_inferior, cota_superior, color='gray', alpha=0.3, label='Región factibilidad')
# # elimina el 60
# # iteraciones.pop()
# # Añadir puntos en las líneas para destacar
# plt.scatter(iteraciones, modelo_A, color='b', s=20)
# plt.scatter(iteraciones, modelo_B, color='g', s=20)

# # Añadir líneas horizontales para las cotas y la región de factibilidad
# ax = plt.gca()  # Obtener el eje actual
# ax.axhline(y=cota_inferior, color='red', linestyle='--', label='Cota Inferior')
# ax.axhline(y=cota_superior, color='red', linestyle='--', label='Cota Superior')
# ax.axhline(y=aprox, color='yellow', linestyle='-', label='Método de aproximación')
# # ax.set_xlim([0, 60])

# # Personalizar la gráfica
# plt.xlabel('Iteraciones')
# plt.ylabel('Vertido (kWh)')
# plt.title('Comparación entre SLSQP y SLSQP inicializado en función de iteraciones')
# plt.legend()
# plt.grid(True)

# # Guardar la gráfica en un archivo de alta calidad
# plt.savefig('comparacion_modelos3.pdf', bbox_inches='tight')







#############################################################################################################################
# Graficos de ruido


