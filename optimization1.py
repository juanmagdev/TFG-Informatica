import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Leer el DataFrame con los datos
data = pd.read_csv('final_data.csv')  # Reemplaza 'tu_archivo.csv' con la ubicación de tu archivo CSV
data = data.iloc[:, 1:]  # Seleccionar todas las filas y las columnas desde la cuarta hacia adelante

# Convertir los datos a un arreglo NumPy
E = data.to_numpy()
n_rows, n_cols = E.shape
total_e = np.random.uniform(1, 4, n_cols)
print(total_e)
print(data)

# Función objetivo
def objective_function(c):
    c_matrix = c.reshape((n_rows, n_cols))
    total = 0
    for j in range(n_cols):
        for i in range(n_rows):
            total += max(0, c_matrix[i, j] * total_e[j] - E[i, j])
    return total

# creo matriz c con todos los valores a 0,25
c_base = np.full((n_rows, n_cols), 0.25)
nDay=30
print("Desperdicio inicial en ",nDay, "dias:" , objective_function(c_base).round(2))

# Restricciones de igualdad
def equality_constraint1(c):
    return np.sum(c.reshape((n_rows, n_cols)), axis=0) - 1
def equality_constraint2(c):
    return np.sum(c.reshape((n_rows, n_cols)), axis=1) - nDay*24/4

bounds = [(0, None)] * (n_rows * n_cols)

# Inicialización aleatoria de los coeficientes
initial_guess = np.full(n_rows * n_cols, 0.25)

# Definir las restricciones
constraints = ({'type': 'eq', 'fun': equality_constraint1},
               {'type': 'eq', 'fun': equality_constraint2})

# Resolver el problema de optimización
res = minimize(objective_function, initial_guess, bounds=bounds, constraints=constraints)

# Obtener la solución óptima
c_optimal = res.x.reshape((n_rows, n_cols))

print("Solución óptima:")
print(c_optimal)
print("Desperdicio finalen ",nDay, "dias:", objective_function(c_optimal).round(2))

# Crear un DataFrame de pandas con los coeficientes
coeficientes_df = pd.DataFrame(c_optimal, columns=[f'c{j}' for j in range(1, n_cols + 1)])

# Guardar el DataFrame en un nuevo archivo CSV
coeficientes_df.to_csv('coeficientes.csv', index=False)
