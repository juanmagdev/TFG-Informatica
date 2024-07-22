import pandas as pd
from scipy.stats import wilcoxon
from autorank import autorank, create_report, plot_stats
import matplotlib.pyplot as plt

# Cargar los datos desde los archivos CSV
results_method_1 = pd.read_csv('coefficients/optimization2_SLSQP.csv')
results_method_2 = pd.read_csv('coefficients/optimization2_custom.csv')

# Aplanar los datos para que cada matriz sea tratada como un conjunto único de muestras
data_1 = results_method_1.values.flatten()
data_2 = results_method_2.values.flatten()

# Wilcoxon Test
# Realiza el test de Wilcoxon para las matrices aplanadas
stat, p_value = wilcoxon(data_1, data_2)
print(f"Estadístico de Wilcoxon: {stat}, p-valor: {p_value}")

