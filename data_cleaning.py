import pandas as pd

# Configuracion ruta
file = '1'
rute = 'source_data/File'+ file + '.txt'
df = pd.read_csv(rute, sep = ' ', names=["UserId", "DateInfo", "ConsumedEnergy"])

# Divido la columna Date Info en 2 columnas, una para el dia (3 primeros digitos) y otra para la hora (2 ultimos digitos), y elimino DateInfo
df['Day'] = df['DateInfo'].apply(lambda x: int(str(x)[:-2]))
df['Hour'] = df['DateInfo'].apply(lambda x: int(str(x)[-2:]))
df.drop(columns=['DateInfo'], inplace=True)

# Como se puede ver, hay valores que tienen hora superior a 48, en estos casos, desecho esas filas
df = df[df['Hour'] <= 48] # Solo me quedo con los que tienen intervalo de 1 a 48

# Paso de kwh a wh, multiplicando por 1000 y trunco a enteros
# df['ConsumedEnergy'] = (df['ConsumedEnergy'] * 1000)

# Crear una tabla pivote
pivot_df = df.pivot_table(index=['UserId', 'Day'], columns='Hour', values='ConsumedEnergy', aggfunc='first')

# Rellenar los valores nulos con el valor de la siguiente columna, luego la anterior, y finalmente con 0
pivot_df = pivot_df.fillna(method='bfill', axis=1).fillna(method='ffill', axis=1).fillna(0)

# Ajustar el rango de horas a 1-48
pivot_df.columns = range(1, 49)

## PASAMOS DE 48 a 24 columnas

# Crear una lista de columnas para agrupar en pares
column_pairs = [(i, i + 1) for i in range(1, 48, 2)]

# Crear una nueva tabla pivote con las medias de las columnas agrupadas
hourly_df = pd.DataFrame()
for hour, (col1, col2) in enumerate(column_pairs, start=0):
    hourly_df[hour] = (pivot_df[col1] + pivot_df[col2])

hourly_df.to_csv('hourly_data.csv')

# Calcular la desviación estándar para cada usuario
std_per_user = hourly_df.groupby('UserId').std()

# Seleccionar los n usuarios con las mayores desviaciones estándar
nUser = 4
top_users = std_per_user.nlargest(nUser, columns=range(0, 24)).index

# Filtrar los datos para quedarnos solo con los usuarios seleccionados
sample_df = hourly_df[hourly_df.index.get_level_values('UserId').isin(top_users)]


# Ordeno sample data por day y luego por user id
sample_df = sample_df.reset_index().sort_values(by=['Day', 'UserId'])

# Me quedo con las nUser primeras filas, n dias
nDay=30
sample_df = sample_df.head(nUser*nDay)

sample_df.to_csv('sample_data.csv')

print("Datos de los 4 usuarios con mayor variabilidad en el consumo de energía han sido guardados en 'sample_data.csv'")

# creo un dataset nuevo con 24*30 columnas, 4 filas, es decir, pongo las horas de cada usuarios seguidas en una fila

# Crear un nuevo dataframe con los datos de consumo de energía de los usuarios seleccionados
# creo 24 primera columnas como D1-H1 D1-H2 ... D1-H24 y luego D2-H1 D2-H2 ... D2-H24 y asi sucesivamente hasta D30-H24
# y luego las 4 filas con los datos de los 4 usuarios
df = sample_df

df_melted = pd.melt(df, id_vars=['UserId', 'Day'], var_name='Hour', value_name='Value')
df_melted['Day_Hour'] = df_melted['Day'].astype(str) + '-'+ df_melted['Hour'].astype(str)
df_pivot = df_melted.pivot_table(index='UserId', columns='Day_Hour', values='Value', aggfunc='first')
sorted_columns = sorted(df_pivot.columns, key=lambda x: tuple(map(int, x.split('-'))))

df_pivot = df_pivot[sorted_columns]

print(df_pivot)
df_pivot.to_csv('final_data.csv')
