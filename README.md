
# Implementación de Modelos de Inteligencia Artificial para Optimizar el Autoconsumo Energético y Minimizar Vertidos a la Red

## Manual de Instalación 📦

### Instalación de librerías de Python 🐍

El desarrollo se ha realizado utilizando Python, y se ha hecho uso de archivos Python y Jupyter Notebooks. Asumiendo que ya tiene instalados Python3 y pip3 en su sistema, instale las siguientes librerías utilizando pip:

```bash
pip3 install pandas==1.5.3 numpy==1.26.4 scipy==1.13.0
```

### Instalación de Jupyter 📓

Jupyter es fundamental para trabajar con notebooks interactivos. Instale Jupyter utilizando pip con el siguiente comando:

```bash
pip3 install jupyter
```

### Verificación de la instalación ✅

Para verificar que todas las librerías están correctamente instaladas, inicie Jupyter Notebook ejecutando el siguiente comando:

```bash
jupyter notebook
```

Esto abrirá Jupyter en su navegador web predeterminado. Cree un nuevo notebook y pruebe importar las librerías con el siguiente código:

```python
import pandas as pd
import numpy as np
import scipy.optimize as opt
```

Si no encuentra errores al importar estas librerías, entonces la instalación ha sido exitosa.

### Mantenimiento de las librerías 🔄

El software ha sido probado con las versiones específicas de las librerías mencionadas anteriormente. Se recomienda mantener sus librerías actualizadas para beneficiarse de mejoras y correcciones de errores, lo cual puede hacerse con el siguiente comando:

```bash
pip3 install --upgrade pandas numpy scipy jupyter
```

Sin embargo, tenga en cuenta que las futuras actualizaciones de estas librerías podrían hacer que parte del código quede obsoleto.

## Documentación 📚

### Estructura del Proyecto 📁

El proyecto consta de varios componentes estructurados en directorios que facilitan la organización y ejecución del software de optimización. A continuación, se describen los principales directorios y archivos:

#### Directorios y archivos principales 📂

- **Raíz del Proyecto:** Contiene los archivos `optimization.ipynb` y `energy_data_processing.py`. El notebook `optimization.ipynb` maneja toda la lógica de optimización, mientras que `energy_data_processing.py` se encarga del preprocesamiento de datos.
- **coefficients:** Este directorio almacena archivos CSV con los coeficientes utilizados por cada método de optimización. Los nombres de los archivos reflejan el tipo de optimización y el método utilizado:
    - `optimization1_SLSQP.csv:` Coeficientes para el modelo de minimización de vertido de energía en kWh usando el algoritmo SLSQP.
    - `optimization1_custom.csv:` Coeficientes para el modelo que minimiza el vertido de energía en kWh usando un método de aproximación personalizado.
    - `optimization1_SLSQP_init.csv:` Coeficientes iniciales usados para alimentar la solución SLSQP, basados en la salida de otro método de SLSQP.
    - `optimization2_SLSQP.csv:` Coeficientes para el modelo de minimización de vertido monetario en euros usando el algoritmo SLSQP.
    - `optimization2_custom.csv:` Coeficientes para el modelo que minimiza el vertido monetario en euros usando un método de aproximación personalizado.
    - `optimization2_SLSQP_init.csv:` Coeficientes iniciales usados para alimentar la solución SLSQP, basados en la salida de otro método de SLSQP.
- **grafics:** Contiene scripts de Python que generan las gráficas utilizadas en la documentación del proyecto.
- **output_files:** Guarda los archivos CSV generados con los datos de consumo procesados.
- **source_data:** Incluye archivos de datos en bruto desde `File1.txt` hasta `File6.txt`, así como datos de generación por defecto.

### Notebook de Optimización 🔧

El archivo `optimization.ipynb` en la raíz del proyecto es fundamental para la ejecución de la optimización. Contiene varios parámetros configurables que el usuario puede ajustar según sea necesario. Los parámetros modificables incluyen:

#### Parámetros configurables ⚙️

- **file_number:** Refiere al número de archivo de datos en bruto. Si se importan los 6 archivos `File1.txt` hasta `File6.txt` se podrá seleccionar cualquier archivo usando este parámetro.
- **n_days:** Número de días para los cuales se generan los datos. Fijo a 30 días para evitar errores de generación.
- **n_users:** Número de usuarios para ser tratados.
- **selection_type:** Tipo de selección de usuarios. Opciones disponibles: `low`, `top`, `random`. Esta opción busca usuarios con muy poca similitud, mucha similitud o aleatorio, en términos de consumos.
- **optimization1:** Activa la optimización para minimizar el desperdicio de energía.
- **optimization2:** Activa la optimización para minimizar el desperdicio monetario en euros.
- **max_iter:** Número máximo de iteraciones permitidas en la optimización. Aconsejable entre 10 y 20 para muestras pequeñas de usuarios (menos de 8 usuarios).
- **system_coefficients:** Coeficientes de participación de cada usuario. Si se deja vacío, se asume equidistante.

#### Ejecución ▶️

El archivo está diseñado para ser ejecutado de manera secuencial y en el orden establecido. Intentar ejecutar bloques de código de forma aislada puede resultar en errores debido a dependencias entre las secciones del código.

El proceso de preprocesamiento de datos es intensivo en el uso de memoria RAM. Ejecutar este archivo en máquinas con recursos limitados de memoria puede ocasionar problemas de rendimiento o fallos. Se recomienda utilizar un sistema con una capacidad de memoria adecuada. Idealmente 16 GB de RAM, y como requisito mínimo 8 GB de RAM.

El número de usuarios y la cantidad de iteraciones configuradas influyen directamente en el tiempo de computación debido a la complejidad temporal del algoritmo SLSQP. Configuraciones con muchos usuarios y un alto número de iteraciones pueden resultar en tiempos de ejecución prolongados. Es aconsejable ajustar estos parámetros según las capacidades del hardware disponible para mantener un balance entre precisión y eficiencia en el tiempo de procesamiento.

### Nota sobre Datos de Consumo 📈

Los datos de consumo en bruto no se pueden proporcionar directamente debido a restricciones del proveedor, pero están disponibles para descarga en la siguiente URL:

[Datos de Consumo](https://www.ucd.ie/issda/data/commissionforenergyregulationcer/)
