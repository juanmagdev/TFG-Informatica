import pandas as pd

# Configuracion ruta
file = '1'
rute = 'source_data/File'+ file + '.txt'
df = pd.read_csv(rute, sep = ' ', names=["UserId", "DateInfo", "ConsumedEnergy"])

#    User ID  Date Info  Consumed Energy
# 0     1392      19503            0.140
# 1     1392      19504            0.138
# 2     1392      19505            0.140
# 3     1392      19506            0.145
# 4     1392      19507            0.145

# Divido la columna Date Info en 2 columnas, una para el dia (3 primeros digitos) y otra para la hora (2 ultimos digitos), y elimino DateInfo
df['Day'] = df['DateInfo'].apply(lambda x: int(str(x)[:-2]))
df['Hour'] = df['DateInfo'].apply(lambda x: int(str(x)[-2:]))
df.drop(columns=['DateInfo'], inplace=True)
print(df.head())

#    UserId  ConsumedEnergy  Day  Hour
# 0    1392           0.140  195     3
# 1    1392           0.138  195     4
# 2    1392           0.140  195     5
# 3    1392           0.145  195     6
# 4    1392           0.145  195     7


# Como se puede ver, hay valores que tienen hora superior a 48, en estos casos, desecho esas filas
df = df[df['Hour'] <= 48] # Solo me quedo con los que tienen intervalo de 1 a 48

# Crear una tabla pivote
pivot_df = df.pivot_table(index=['UserId', 'Day'], columns='Hour', values='ConsumedEnergy', aggfunc='first')

# Rellenar los valores nulos con el valor de la siguiente columna, luego la anterior, y finalmente con 0
pivot_df = pivot_df.fillna(method='bfill', axis=1).fillna(method='ffill', axis=1).fillna(0)

print(pivot_df.head())

# Ajustar el rango de horas a 1-48
pivot_df.columns = range(1, 49)

print(pivot_df.head())

## PASAMOS DE 48 a 24 columnas

# Crear una lista de columnas para agrupar en pares
column_pairs = [(i, i + 1) for i in range(1, 48, 2)]

# Crear una nueva tabla pivote con las medias de las columnas agrupadas
hourly_df = pd.DataFrame()
for hour, (col1, col2) in enumerate(column_pairs, start=1):
    hourly_df[hour] = (pivot_df[col1] + pivot_df[col2]) / 2

print(hourly_df.head())
