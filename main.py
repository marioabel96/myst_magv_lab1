# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 1: Inversión de Capital                                                        -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: marioabel96                                                                                 -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/marioabel96/myst_magv_lab1                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
#%%
from data import *
from functions import *
import pandas as pd
import numpy as np
from os import listdir, path
from os.path import isfile, join


#%% # Lectura de archivos en carpeta "files"

# Obtener ruta de los archivos
abspath = path.abspath("files/")

# Obtener nombres de los archivos
files = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
files = ["NAFTRAC_" + i.strftime("%Y%m%d") for i in sorted(pd.to_datetime(files))]

# Generar data frame con datos del Naftrac
naftrac_complete = df_of_data(files)

# Obtener todas las fechas
dates = get_dates(files)

# Convertimos activos a cash (KOFL.MX, KOFUBL.MX, USD.MXN, BSMXB.MX, NMKA.MX )
# Por el momento solo las quite para calcular despues el faltante
naftrac_complete = conversion_cash(naftrac_complete) 

# Creamos un nuevo df con solo las columnas que necesitaremos
naftrac_stats = naftrac_complete[['Ticker', 'Peso (%)', 'Fecha']]

# Creamos lista de todos los tickers
all_tickers = list(naftrac_stats['Ticker'].unique())



#%%
# Descargamos los precios de los ticker en el dia de rebalanceo



#%%
#-------------------------------------------
#-- Inversión Pasiva NAFTRAC
comision = 0.00125 # (títulos*precio*comisión).
capital = 1000000
## Calcular el val del portafolio para todas las fechas con los archivos historicos
## Pre-pandemia 31-01-2018 a 31-01-2020 df_pasiva_a
## En-Pandemia  28-02-2020 a 28-02-2021 df_pasiva_b




#-------------------------------------------
#-- Inversión Activa
# Tabla de historico operaciones
# Tabla medidas de atribución al desempeño

# %%
