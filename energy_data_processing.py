import pandas as pd
import os

OUTPUT_DIR = 'output_files'

def read_data(file_number):
    """
    Lee los datos del archivo correspondiente y realiza las transformaciones necesarias.
    Devuelve el DataFrame resultante.
    """
    file_path = f'source_data/File{file_number}.txt'
    df = pd.read_csv(file_path, sep=' ', names=["UserId", "DateInfo", "ConsumedEnergy"])
    df['Day'] = df['DateInfo'].apply(lambda x: int(str(x)[:-2]))
    df['Hour'] = df['DateInfo'].apply(lambda x: int(str(x)[-2:]))
    df.drop(columns=['DateInfo'], inplace=True)
    df = df[df['Hour'] <= 48]
    df = df[(df['Day'] >= 195) & (df['Day'] <= 224)]
    pivot_df = df.pivot_table(index=['UserId', 'Day'], columns='Hour', values='ConsumedEnergy', aggfunc='first')
    # pivot_df = pivot_df.fillna(method='bfill', axis=1).fillna(method='ffill', axis=1).fillna(0)
    pivot_df.columns = range(1, 49)
    return pivot_df

def group_hours(pivot_df):
    """
    Agrupa las horas en pares y calcula la media de cada par.
    Devuelve el DataFrame resultante.
    """
    column_pairs = [(i, i + 1) for i in range(1, 48, 2)]
    hourly_df = pd.DataFrame()
    for hour, (col1, col2) in enumerate(column_pairs, start=0):
        hourly_df[hour] = (pivot_df[col1] + pivot_df[col2])
    return hourly_df

def select_top_users(hourly_df, n_users):
    """
    Calcula la desviación estándar para cada usuario y selecciona los n usuarios con las mayores desviaciones estándar.
    Devuelve el DataFrame resultante.
    """
    std_per_user = hourly_df.std(axis=1)
    # top_users = std_per_user.nlargest(n_users, columns=range(0, 24)).index
    top_users = std_per_user.nlargest(n_users).index # cambiar por nlargest
    return top_users

# metodo para seleccionar los usuarios con consumo mas parecido
def select_random_users(hourly_df, n_users):
    """
    Calcula la desviación estándar para cada usuario y selecciona los n usuarios con las menores desviaciones estándar.
    Devuelve el DataFrame resultante.
    """
    random_users = hourly_df.sample(n=n_users).index
    return random_users


def filter_data(hourly_df, top_users, n_days):
    """
    Filtra los datos para quedarse solo con los usuarios seleccionados y los primeros n días.
    Devuelve el DataFrame resultante.
    """
    sample_df = hourly_df[hourly_df.index.get_level_values('UserId').isin(top_users)]
    sample_df = sample_df.reset_index().sort_values(by=['Day', 'UserId']).head(len(top_users) * n_days)
    return sample_df

def reshape_data(sample_df):
    """
    Reshapea los datos para tener las horas de cada usuario seguidas en una fila.
    Devuelve el DataFrame resultante.
    """
    df_melted = pd.melt(sample_df.reset_index(), id_vars=['UserId', 'Day'], var_name='Hour', value_name='Value')
    df_melted['Day_Hour'] = df_melted['Day'].astype(str) + '-' + df_melted['Hour'].astype(str)
    df_pivot = df_melted.pivot_table(index='UserId', columns='Day_Hour', values='Value', aggfunc='first')
    sorted_columns = sorted(df_pivot.columns, key=lambda x: tuple(map(int, x.split('-'))))
    df_pivot = df_pivot[sorted_columns]
    return df_pivot

def save_final_data(df, file_name):
    """
    Guarda el DataFrame en un archivo CSV.
    """
    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path)

def select_low_variance_users(reshaped_df, n_users):
    """
    Selecciona un conjunto de usuarios con menor desviación estándar en el consumo.
    """
    std_per_user = reshaped_df.std(axis=1)
    low_variance_users = std_per_user.nsmallest(n_users).index
    return low_variance_users

def filter_users_by_consumption(reshaped_df, min_consumption=1000, max_consumption=2000):
    """
    Filtra usuarios con una suma de consumos entre `min_consumption` y `max_consumption`.
    """
    total_consumption = reshaped_df.sum(axis=1)
    filtered_users = total_consumption[(total_consumption >= min_consumption) & (total_consumption <= max_consumption)].index
    return reshaped_df.loc[filtered_users]

def main(file_number, n_users, selection_type):
    if selection_type == 'top':
        output_file = 'final_data_File' + str(file_number) + '_Users' + str(n_users) +'_Top.csv'
    elif selection_type == 'low':
        output_file = 'final_data_File' + str(file_number) + '_Users' + str(n_users) +'_Low.csv'
    elif selection_type == 'random':
        output_file = 'final_data_File' + str(file_number) + '_Users' + str(n_users) +'_Random.csv'
    else:
        raise ValueError("Tipo de selección no válido: elija 'top', 'low' o 'random'.")
    pivot_df = read_data(file_number)
    hourly_df = group_hours(pivot_df)
    reshaped_df = reshape_data(hourly_df)

    reshaped_df = filter_users_by_consumption(reshaped_df, 500, 2000)
    # elimina las filas que tengan algun valor NaN
    reshaped_df.dropna(inplace=True)


    # Selecciona usuarios basado en la desviación estándar después de reorganizar el DataFrame
    if selection_type == 'top':
        selected_users = select_top_users(reshaped_df, n_users)
    elif selection_type == 'low':
        selected_users = select_low_variance_users(reshaped_df, n_users)
        print(selected_users)
    elif selection_type == 'random':
        selected_users = select_random_users(reshaped_df, n_users)

    filtered_df = reshaped_df.loc[selected_users]

    # Guardar los datos finales
    save_final_data(filtered_df, output_file)
    print(f"Los datos han sido guardados en '{output_file}'")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_number = '1'
    n_users = 3
    selection_type = 'low'
    main(file_number, n_users, selection_type)