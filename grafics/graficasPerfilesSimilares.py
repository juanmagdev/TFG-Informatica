
import matplotlib.pyplot as plt
# Datos de ejemplo 
# 1205    518.889
# 1224    243.963
# 1472    668.073
# 1743    621.568

# PARA 4 USUARIOS LOW
iteraciones = [2, 3, 4, 5, 6, 8, 10, 14, 18]
modelo_A =  [465.63, 307.39, 222.67, 151.58, 136.12, 94.78, 47.19, 37.54, 31.15]
modelo_B =  [70.43,56.02, 53.06, 48.28, 41.53, 37.85, 30.2, 25, 19.21]
cota_superior = 113.57
cota_inferior = 0  # Cota inferior para cada iteración
aprox = 115.62
additional_info = 'Usuarios    Consumo\n   1175       1707.021\n   1335       1435.750\n   1503       1623.742\n   1443       1264.492'

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(12, 5))


# GRAFICA ITERACIONES

# Graficar las series con líneas
plt.plot(iteraciones, modelo_A, 'r-', label='SLSQP')
plt.plot(iteraciones, modelo_B, 'b-', label='SLSQP Inicializado')
# iteraciones.append(60)
plt.fill_between(iteraciones, cota_inferior, cota_superior, color='gray', alpha=0.3, label='Región factibilidad')

plt.scatter(iteraciones, modelo_A, color='r', s=20, label='Puntos SLSQP')
plt.scatter(iteraciones, modelo_B, color='b', s=20, label='Puntos SLSQP Inicializado')

# Añadir líneas horizontales para las cotas y la región de factibilidad
ax = plt.gca()  # Obtener el eje actual
ax.axhline(y=cota_inferior, color='red', linestyle='--', label='Cota Inferior')
ax.axhline(y=cota_superior, color='orange', linestyle='--', label='Cota Superior')
ax.axhline(y=aprox, color='yellow', linestyle='-', label='Método de aproximación')
# ax.set_xlim([0, 60])

# Personalizar la gráfica
plt.xlabel('Iteraciones')
plt.ylabel('Vertido (kWh)')
plt.title('Comparación entre SLSQP y SLSQP inicializado en función de iteraciones')
plt.legend()
plt.grid(True)
plt.text(0.1, 0.7, additional_info, transform=plt.gca().transAxes, fontsize=11,
         bbox=dict(facecolor='white', alpha=0.7))

# Guardar la gráfica en un archivo de alta calidad
plt.savefig('graficaLow.pdf', bbox_inches='tight')