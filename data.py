# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 1: Inversión de Capital                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: marioabel96                                                                                 -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/marioabel96/myst_magv_lab1                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import pandas as pd
import numpy as np
from os import listdir, path
from os.path import isfile, join

#%% Read all the files in "files" folder
#abspath = path.abspath("files/")

#files = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
#files = ["NAFTRAC_" + i.strftime("%Y%m%d") for i in sorted(pd.to_datetime(files))]



#%% Read and store all the files in a dict
def df_of_data(files):
    data_files = {}

    for i in files:
        print("i: ", i, "leido ok")
        data = pd.read_csv("files/" + i + ".csv", skiprows=2, header=0)
        # Acomodo de datos tickers para futuras descargas en YFinance
        data['Ticker'] = [i.replace("*","") for i in data["Ticker"]]
        data['Ticker'] = data['Ticker'] + '.MX'

        # Añadir columna fecha  
        data['Fecha'] = i
        data['Fecha'] = [i.replace('NAFTRAC_','') for i in data['Fecha']]
        data['Fecha'] = [i.replace('.csv','') for i in data['Fecha']]

        # Cambiar peso a numerico
        data['Peso (%)'] = [i/100 for i in data["Peso (%)"]]
        data_files[i] = data

    # Crear df con los datos 
    naftrac = pd.concat(data_files)

    # Quitar Nans
    naftrac.dropna(subset = ["Nombre"], inplace=True)

    # Convertir Fecha a datetime
    naftrac['Fecha'] = pd.to_datetime(naftrac['Fecha'],format='%Y%m%d')

    #return naftrac
    return naftrac


def conversion_cash(df): 
    # Cambiamos tickers a cash (KOFL.MX, KOFUBL.MX, USD.MXN, BSMXB.MX, NMKA.MX )
    deltickers = ['KOFL.MX', 'KOFUBL.MX', 'USD.MX', 'BSMXB.MX', 'NMKA.MX','NEMAKA.MX']
    df = df[~df['Ticker'].isin(deltickers)]

    return df
# %%
