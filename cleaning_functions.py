import pandas as pd

def load_data(file):
    """
    Carga los datos desde un archivo y realiza la limpieza inicial.
    
    Args:
    - file: El nombre del archivo a cargar.
    
    Returns:
    - df: El DataFrame limpio.
    """
    rute = 'source_data/File' + str(file) + '.txt'
    df = pd.read_csv(rute, sep=' ', names=["UserId", "DateInfo", "ConsumedEnergy"])
    df['Day'] = df['DateInfo'].apply(lambda x: int(str(x)[:-2]))
    df['Hour'] = df['DateInfo'].apply(lambda x: int(str(x)[-2:]))
    df.drop(columns=['DateInfo'], inplace=True)
    return df

def preprocess_data(df):
    """
    Realiza el preprocesamiento de los datos.
    
    Args:
    - df: El DataFrame con los datos sin procesar.
    
    Returns:
    - hourly_df: El DataFrame preprocesado.
    """
    df = df[df['Hour'] <= 48]
    pivot_df = df.pivot_table(index=['UserId', 'Day'], columns='Hour', values='ConsumedEnergy', aggfunc='first')
    pivot_df = pivot_df.fillna(method='bfill', axis=1).fillna(method='ffill', axis=1).fillna(0)
    pivot_df.columns = range(1, 49)
    column_pairs = [(i, i + 1) for i in range(1, 48, 2)]
    hourly_df = pd.DataFrame()
    for hour, (col1, col2) in enumerate(column_pairs, start=1):
        hourly_df[hour] = (pivot_df[col1] + pivot_df[col2]) / 2
    return hourly_df

def select_users(hourly_df, n_users=4):
    """
    Selecciona los usuarios con la mayor variabilidad en el consumo de energía.
    
    Args:
    - hourly_df: El DataFrame preprocesado.
    - n_users: El número de usuarios a seleccionar.
    
    Returns:
    - sample_df: El DataFrame con los datos de los usuarios seleccionados.
    """
    std_per_user = hourly_df.groupby('UserId').std()
    top_users = std_per_user.nlargest(n_users, columns=range(1, 25)).index
    sample_df = hourly_df[hourly_df.index.get_level_values('UserId').isin(top_users)]
    return sample_df

def save_data(df, filename='sample_data.csv'):
    """
    Guarda los datos en un archivo CSV.
    
    Args:
    - df: El DataFrame con los datos a guardar.
    - filename: El nombre del archivo CSV.
    """
    df.to_csv(filename)
    print(f"Los datos han sido guardados en '{filename}'")
