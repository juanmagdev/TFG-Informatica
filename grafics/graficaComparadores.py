import matplotlib.pyplot as plt

refined_p_values_cases = [
    [0.0001, 0.0002, 0.0004, 0.1012, 0.2015, 0.3021, 0.5013, 0.6008, 0.7012, 0.8003],
    [0.0002, 0.0003, 0.0005, 0.0915, 0.3017, 0.4022, 0.5501, 0.6509, 0.7504, 0.8510],
    [0.0003, 0.0004, 0.0006, 0.0823, 0.2528, 0.3579, 0.6004, 0.7001, 0.8025, 0.9006],
    [0.0001, 0.0002, 0.0003, 0.0708, 0.2734, 0.3745, 0.5702, 0.6703, 0.7705, 0.8702],
    [0.0004, 0.0005, 0.0006, 0.0632, 0.2651, 0.3680, 0.5608, 0.6607, 0.7609, 0.8605]
]

iterations = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
# Crear la gráfica con valores más precisos
plt.figure(figsize=(12, 6))
for idx, p_values in enumerate(refined_p_values_cases, start=1):
    plt.plot(iterations, p_values, label=f'Test {idx}', marker='o')

# Añadir etiquetas y título
plt.axhspan(0, 0.05, color='yellow', alpha=0.3, label='Región de Significancia Estadística ($p < 0.05$)')
plt.xlabel('Número de Iteraciones')
plt.ylabel('Valor del p-valor')
plt.title('Valores de p-valor por Número de Iteraciones')
plt.legend()
plt.grid(True)

# Especificar las marcas del eje x
plt.xticks(iterations)  # Asegurarse de que solo aparecen números enteros

# Guardar la gráfica en un archivo
plt.savefig('p_value.pdf', bbox_inches='tight')
