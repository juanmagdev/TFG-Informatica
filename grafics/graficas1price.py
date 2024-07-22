import matplotlib.pyplot as plt
from brokenaxes import brokenaxes

# Datos de ejemplo 
# 1590     956.110
# 1972     781.464
# 1085     486.352
# 1181    1298.585

# PARA 4 USUARIOS
iteraciones = [0, 2, 4, 6, 8, 10, 12, 14]
modelo_A = [43.23, 37.94, 12.86, 7.45, 3.92, 1.37, 0.91, 0.54]
time_A = [58.43, 181.00, 476.1, 651.32, 798.45, 1029.10, 1200.55, 1390.72]
modelo_B = [16.83, 8.63, 5.65, 3.48, 1.94, 0.51, 0.30, 0.15]
time_B = [60.12, 197.80, 497.50, 713.64, 935.78, 1242.90, 1400.45, 1600.62]
cota_superior = 34.44
cota_inferior = 0  # Cota inferior para cada iteración
aprox = 16.83
additional_info = 'Usuarios    Consumo\n   1590       956.110\n   1972       781.464\n   1085       486.352\n   1181       1298.585'

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
ax.fill_betweenx([cota_inferior, cota_superior], 0, 30, color='gray', alpha=0.3, label='Región de Factibilidad')

# Añadir título y etiquetas
ax.set_title('Desempeño de SLSQP y SLSQP Inicializado con variable de precio')
ax.set_xlabel('Tiempo (minutos)')
ax.set_ylabel('Vertido (euros)')

# Ajustar los límites del eje x para enfocar solo hasta el minuto 60
# ax.set_xlim([0, 60])

# Añadir leyenda
plt.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))
ax.grid(True)

# Guardar la gráfica en un archivo de alta calidad
plt.text(0.2, 0.7, additional_info, transform=plt.gca().transAxes, fontsize=11,
         bbox=dict(facecolor='white', alpha=0.7))
plt.savefig('desempeno_modelos1price.pdf', bbox_inches='tight')



# GRAFICA ITERACIONES

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
# plt.ylabel('Vertido (euros)')
# plt.title('Comparación entre SLSQP y SLSQP inicializado con variable de precio')
# # plt.legend()
# plt.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))
# plt.grid(True)
# plt.text(0.1, 0.7, additional_info, transform=plt.gca().transAxes, fontsize=11,
#          bbox=dict(facecolor='white', alpha=0.7))

# # Guardar la gráfica en un archivo de alta calidad
# plt.savefig('comparacion_modelos1price.pdf', bbox_inches='tight')







#############################################################################################################################
# Graficos de ruido
