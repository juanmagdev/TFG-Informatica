import pandas as pd
import numpy as np
import energy_optimization_hora as eo

def minimize_waste_Juanma(dataset, energy_generatte):
    """
    Algortimo inventado para optimizar coeficientes de consumo.

    Args:
     - dataset: DataFrame con los datos de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
     - energy_generate: Energía total generada por el sistema de placas solares durante un mes por hora, array de 24*30 elementos.
    
    Returns:
    - coeficientes_df: Coeficientes de reparto de energía para cada usuario, tabla de 4x720 elementos.
     
    """
    coeficientes_df = pd.DataFrame(np.full((4, 720), 0), columns=[f'c{j}' for j in range(1, 721)])

    # Busco la columna, que sumando 3 de las 4 celdas, tiene valor menor de toda la tabla.
    for j in range(720):
        minimo = 100000000
        for i in range(4):
            for k in range(4):
                if i != k:
                    for l in range(4):
                        if i != l and k != l:
                            suma = dataset[i][j] + dataset[k][j] + dataset[l][j]
                            if suma < minimo:
                                print(suma, " con los usuarios ", i, k, l, " y la hora ", j)
                                minimo = suma
                                minimo_i = i
                                minimo_k = k
                                minimo_l = l
                                col_j = j
        # situo 1 en la columna col_j, en la fila que no es ni minimo_i, ni minimo_k, ni minimo_l
        if puedoEscribirEnFila(dataset, coeficientes_df, col_j, minimo_i, minimo_k, minimo_l):
            print(col_j," ---Escribo en la columna ", col_j)
            for i in range(4):
                if i != minimo_i and i != minimo_k and i != minimo_l:
                    print("Escribo en la fila ", i, " y la columna ", col_j)
                    coeficientes_df.iloc[i, col_j] = 1

    # Busco la columna, que sumando 2 de las 4 celdas, tiene valor menor de toda la tabla.
    return coeficientes_df

def puedoEscribirEnFila(dataset, coeficientes, j, minimo_i, minimo_k, minimo_l):
    """
    Función para comprobar que la suma de cada columna de coeficientes sea 180
    Args:
     - coeficientes: DataFrame con los coeficientes de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
    
    Returns:
    - True si la suma de cada fila es 1, False en caso contrario.
     
    """
    if np.sum(coeficientes.iloc[:, j]) == 180:
        print("La suma de la columna ", j, " es 180")
        return False
    for i in range(4):
        if i != minimo_i and i != minimo_k and i != minimo_l:
            if dataset[i, j] <= dataset[minimo_i, j] + dataset[minimo_k, j] + dataset[minimo_l, j]:
                print("No puedo escribir en la fila ", i, " y la columna ", j)
                print("Porque ", dataset[i, j], " es menor que ", dataset[minimo_i, j], " + ", dataset[minimo_k, j], " + ", dataset[minimo_l, j])
                return False
    print("Puedo escribir en la columna ", j)
    print("Porque ", dataset[i, j], " es mayor que ", dataset[minimo_i, j], " + ", dataset[minimo_k, j], " + ", dataset[minimo_l, j])
    return True




def metodo_consumo_mayor_ordenado(E, total_e):
    """
    Algortimo para optimizar coeficientes de consumo.
    La idea es comenzar por la columna 1 hasta la 702 en orden, saturamos la celda con el valor mas alto,
    y vamos a la siguiente columna. Antes de todo se ha de comprobar que se puede escribir en la celda, 
    que la suma de la fila sea menor que 180.
    Args:
     - E: DataFrame con los datos de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
     - total_e: Energía total generada por el sistema de placas solares durante un mes por hora, array de 24*30 elementos.
    
    Returns:
    - coeficientes_df: Coeficientes de reparto de energía para cada usuario, tabla de 4x720 elementos.
     
    """
    coeficientes_df = pd.DataFrame(np.full((4, 720), 0), columns=[f'c{j}' for j in range(1, 721)])
    for j in range(720):
        mayor = 0
        for i in range(4):
            if filaSuma180(coeficientes_df, i, 0)==False:
                if E[i][j] >= mayor:
                    mayor = E[i][j]
                    mayor_i = i
        coeficientes_df.iloc[mayor_i, j] = 1
    return coeficientes_df

def filaSuma180(coeficientes, fila, mod):
    """
    Función para comprobar que la suma de cada columna de coeficientes sea 180
    Args:
     - coeficientes: DataFrame con los coeficientes de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
    
    Returns:
    - True si la suma de cada fila es 1, False en caso contrario.
     
    """
    if np.sum(coeficientes.iloc[fila, :]) < 180-mod:
        return False
    return True


data = pd.read_csv('final_data.csv') 
data = data.iloc[:, 1:]  # Seleccionar todas las filas y las columnas desde la segunda en adelante
E = data.to_numpy()
n_rows, n_cols = E.shape
print(E)


# CARGO DATOS DE GENERACION
import pandas as pd
generacion = pd.read_csv('generacion.csv')
generacion = generacion.dropna()

generacion = generacion.iloc[:,1]

# devuelvo un array con los valores de la unica columna que tiene el dataframe
gen_array = generacion.values
total_e = gen_array

################

total_e = [round(i/1000, 2) for i in total_e]
total_e = np.array(total_e)
resultdf = metodo_consumo_mayor_ordenado(E, total_e)

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

def metodo_consumo_mayor_minimizado(E, total_e):
    """
    Algortimo para optimizar coeficientes de consumo.
    La idea es comenzar por la columna 1 hasta la 702 en orden, tomamos los coeficientes optimos de cada columna. Antes de todo 
    se ha de comprobar que se puede escribir en la celda, 
    que la suma de la fila sea menor que 180.
    Args:
     - E: DataFrame con los datos de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
     - total_e: Energía total generada por el sistema de placas solares durante un mes por hora, array de 24*30 elementos.
    
    Returns:
    - coeficientes_df: Coeficientes de reparto de energía para cada usuario, tabla de 4x720 elementos.
     
    """
    coeficientes_df = pd.DataFrame(np.full((4, 720), 0), columns=[f'c{j}' for j in range(1, 721)])
    ac = 0
    for j in range(720):
        if total_e[j] == 0:
            coeficientes_df.iloc[:, j] = 0.25
            ac += 1
            continue
        consumo = [0, 0, 0, 0]
        for i in range(4):
            # if filaSuma180(coeficientes_df, i, ac*0.25)==False:
            if filaSuma180(coeficientes_df, i, 0)==False:
                consumo[i] = E[i][j]
            else:
                consumo[i] = 0

        if np.count_nonzero(consumo) == 1:
            coeficientes_df.iloc[np.nonzero(consumo)[0][0], j] = 1
        elif np.count_nonzero(consumo) == 2:    # aproximacion cositas
            for i in range(4):
                if consumo[i] != 0:
                    coeficientes_df.iloc[i, j] = 0.5

        else:
            coeficientes, min_waste = eo.optimize_energy_distribution(total_e[j], consumo)
            coeficientes_df.iloc[:, j] = coeficientes
    
    for i in range(4):
        print("La suma de la fila ", i, " es ", np.sum(coeficientes_df.iloc[i, :]))
    return coeficientes_df


c_base = np.full((n_rows, n_cols), 0.25)
nDay=30
resultdf = metodo_consumo_mayor_minimizado(E, total_e)
print("Desperdicio inicial 0,25 en ",nDay, "dias:" , objective_function(c_base).round(2))
print("Desperdicio inicial optimizado sin libreria ",nDay, "dias:" , objective_function(resultdf.to_numpy()).round(2))




# COPIA DE OPTIMIZATION1.PY
from scipy.optimize import minimize
def objective_function(c):
    c_matrix = c.reshape((n_rows, n_cols))
    total = 0
    for j in range(n_cols):
        for i in range(n_rows):
            total += max(0, c_matrix[i, j] * total_e[j] - E[i, j])
    return total

def objective_function_mod(c):
    c_matrix = c.reshape((n_rows, n_cols))
    total = 0
    for j in range(n_cols):
        for i in range(n_rows):
            total -= c_matrix[i, j] * total_e[j] - E[i, j]
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


bounds = [(0, 1)] * (n_rows * n_cols)

# Inicialización de los coeficientes, uso el que devuelve el metodo anterior
initial_guess = np.full(n_rows * n_cols, 0.25)

# Definir las restricciones
constraints = ({'type': 'eq', 'fun': equality_constraint1},
               {'type': 'eq', 'fun': equality_constraint2})

# Resolver el problema de optimización
def callback_function(xk):
    print("Iteración:", callback_function.iteration)
    print("Variables de decisión:", xk)
    print("Valor de la función objetivo:", objective_function(xk))
    print("--------------------------")
    callback_function.iteration += 1

# Inicializa el contador de iteraciones
callback_function.iteration = 0

# Llama a minimize con la función de devolución de llamada especificada
res = minimize(objective_function, initial_guess, bounds=bounds, constraints=constraints, method='SLSQP', callback=callback_function, options={'disp': True})


# Obtener la solución óptima
c_optimal = res.x.reshape((n_rows, n_cols))

print("Solución óptima de minimize:")
print(c_optimal)
print("Desperdicio final en ",nDay, "dias con minimize:", objective_function(c_optimal).round(2))

# Crear un DataFrame de pandas con los coeficientes
coeficientes_df = pd.DataFrame(c_optimal, columns=[f'c{j}' for j in range(1, n_cols + 1)])



def calcula_suma_vertido_energia(total_e, E):
    # array de 720 elementos, todos a 0
    suma_vertido_energia = np.zeros_like(total_e)

    # recorro las 720 columnas
    for j in range(720):
        suma = 0
        generacion = total_e[j]
        for i in range(4):
            consumo = E[i, j]
            if consumo < generacion*0.25:
                suma += generacion*0.25 - consumo
        suma_vertido_energia[j] = suma
    return suma_vertido_energia

def check_orden_decreciente(suma_vertido_energia):
    for j in range(719):
        if suma_vertido_energia[j] < suma_vertido_energia[j+1]:
            return False
    return True


def metodo_consumo_mayor_ordenado_minimizado(E, total_e):
    """
    Algortimo para optimizar coeficientes de consumo.
    La idea es comenzar por la columna 1 hasta la 720 en orden, tomamos los coeficientes optimos de cada columna. Antes de todo 
    se ha de comprobar que se puede escribir en la celda, 
    que la suma de la fila sea menor que 180.
    Args:
     - E: DataFrame con los datos de consumo de energía de los usuarios, donde las filas son los usuarios y las columnas son las horas del día durante un mes, array de 4*720 elementos.
     - total_e: Energía total generada por el sistema de placas solares durante un mes por hora, array de 24*30 elementos.
    
    Returns:
    - coeficientes_df: Coeficientes de reparto de energía para cada usuario, tabla de 4x720 elementos.
     
    """
    suma_vertido_energia = calcula_suma_vertido_energia(total_e, E)
    np.savetxt('suma_vertido_energia.txt', suma_vertido_energia, delimiter=',')    
    orden_columnas = np.argsort(suma_vertido_energia)   # ordena de menor a mayor

    orden_columnas = orden_columnas[::-1]    
    E_ordenado = E[:, orden_columnas]
    
    coeficientes_df_ordenado = metodo_consumo_mayor_minimizado(E_ordenado, total_e)
    return coeficientes_df_ordenado.iloc[:, np.argsort(orden_columnas)]



nDay=30
resultdf = metodo_consumo_mayor_ordenado_minimizado(E, total_e)
print("Desperdicio inicial 0,25 en ",nDay, "dias:" , objective_function(c_base).round(2))
print("Desperdicio inicial optimizado sin libreria ordenado J ",nDay, "dias:" , objective_function(resultdf.to_numpy()).round(2))




