import pandas as pd
import numpy as np
from scipy.optimize import minimize

def optimization_function(coef, total_energy, consumed_energy):
    """
    Función de optimización para minimizar el desperdicio de energía a la red.
    
    Args:
    - coef: Coeficientes de reparto de energía para cada usuario.
    - total_energy: Energía total generada por el sistema de placas solares.
    - consumed_energy: Energía consumida por cada usuario.
    
    Returns:
    - waste: Desperdicio total de energía a la red.
    """

    if np.abs(np.sum(coef) - 1) > 1e-6:
        return np.inf
    
    assigned_energy = coef * total_energy
    waste = np.maximum(0, assigned_energy - consumed_energy)
    total_waste = np.sum(waste)
    
    return total_waste


def optimize_energy_distribution(total_energy, consumed_energy):
    """
    Optimiza la distribución de energía entre los usuarios para minimizar el desperdicio de energía a la red.
    
    Args:
    - total_energy: Energía total generada por el sistema de placas solares.
    - consumed_energy: Energía consumida por cada usuario.
    
    Returns:
    - optimized_coef: Coeficientes de reparto de energía óptimos.
    - min_waste: Desperdicio mínimo de energía a la red.
    """

    n_users = len(consumed_energy)
    initial_coef = np.ones(n_users) / n_users
    
    # x = vector de coeficientes
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                   {'type': 'ineq', 'fun': lambda x: x}, 
                   {'type': 'ineq', 'fun': lambda x: x*total_energy - consumed_energy})
    
    constraints2 = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
               {'type': 'ineq', 'fun': lambda x: x})
    
    result = minimize(optimization_function, initial_coef, args=(total_energy, consumed_energy),
                      constraints=constraints, bounds=[(0, 1)] * n_users)
    
    optimized_coef = result.x
    min_waste = result.fun
    
    return optimized_coef, min_waste


def optimize_energy_distribution_hard(total_energy, consumed_energy):
    """
    Optimiza la distribución de energía entre los usuarios para minimizar el desperdicio de energía a la red.
    
    Args:
    - total_energy: Energía total generada por el sistema de placas solares.
    - consumed_energy: Energía consumida por cada usuario.
    
    Returns:
    - optimized_coef: Coeficientes de reparto de energía óptimos.
    - min_waste: Desperdicio mínimo de energía a la red.
    """
    n_users = len(consumed_energy)
    best_waste = np.inf
    best_coef = None

    egality_coef = consumed_energy / n_users

    for coef1 in np.linspace(0, 1, 101):
        if (egality_coef[0] < 0.25) : coef1 = egality_coef[0]

        for coef2 in np.linspace(0, 1 - coef1, 101):
            if (egality_coef[1] < 0.25) : coef2 = egality_coef[1]

            for coef3 in np.linspace(0, 1 - coef1 - coef2, 101):
                if (egality_coef[2] < 0.25) : coef3 = egality_coef[2]

                coef4 = 1 - coef1 - coef2 - coef3
                if (egality_coef[3] < 0.25) : coef4 = egality_coef[3]

                coef = np.array([coef1, coef2, coef3, coef4])
                assigned_energy = coef * total_energy
                waste = np.maximum(0, assigned_energy - consumed_energy)
                total_waste = np.sum(waste)


                if total_waste < best_waste:
                    best_waste = total_waste
                    best_coef = coef.copy()
    
    return best_coef, best_waste


# EJEMPLO USO

total_energy = 4
consumed_energy = np.array([0.614, 0.193, 3.146, 2.919])
initial_coef = np.ones(4) / 4 # Coeficientes iniciales 0,25 cada uno

result = optimization_function(initial_coef, total_energy, consumed_energy)
print("Desperdicio total de energía a la red:", result)

# USUARIO                             A          B          C          D
# Coeficientes de reparto óptimos: [0.1535     0.04825    0.40745252 0.39079748]
# Desperdicio mínimo de energía a la red: 0.0
# [0.1535     0.04825    0.40745252 0.39079748] * 4 = [0.614      0.193      1.62981008 1.56318992] <=  [0.614, 0.193, 3.146, 2.919]

print("\nEjemplo de uso por minimización:")
optimized_coef, min_waste = optimize_energy_distribution(total_energy, consumed_energy)
print("Coeficientes de reparto óptimos:", optimized_coef)
print("Desperdicio mínimo de energía a la red:", min_waste)


print("\nEjemplo de uso por fuerza bruta:")
optimized_coef, min_waste = optimize_energy_distribution_hard(total_energy, consumed_energy)
print("Coeficientes de reparto óptimos:", optimized_coef)
print("Desperdicio mínimo de energía a la red:", min_waste)





