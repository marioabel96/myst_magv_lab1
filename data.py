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
import pandas_datareader.data as web
import yfinance as yf

# Read all the files in "files" folder
#abspath = path.abspath("files/")

#files = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
#files = ["NAFTRAC_" + i.strftime("%Y%m%d") for i in sorted(pd.to_datetime(files))]



# Read and store all the files in a dict
def df_of_data(files):
    data_files = {}

    for i in files:
        #print("i: ", i, "leido ok")
        data = pd.read_csv("files/" + i + ".csv", skiprows=2, header=0)
        # Acomodo de datos tickers para futuras descargas en YFinance
        data['Ticker'] = [i.replace("*","") for i in data["Ticker"]]
        data['Ticker'] = data['Ticker'] + '.MX'

        # Añadir columna fecha  
        data['Date'] = i
        data['Date'] = [i.replace('NAFTRAC_','') for i in data['Date']]
        data['Date'] = [i.replace('.csv','') for i in data['Date']]

        # Cambiar peso a numerico
        data['Peso (%)'] = [i/100 for i in data["Peso (%)"]]
        data_files[i] = data

    # Crear df con los datos 
    naftrac = pd.concat(data_files)

    # Quitar Nans
    naftrac.dropna(subset = ["Nombre"], inplace=True)

    # Remplazar tickets que cambiaron de nombre para la funcion de precios
    naftrac['Ticker'] = naftrac['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
    naftrac['Ticker'] = naftrac['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
    naftrac['Ticker'] = naftrac['Ticker'].replace('SITESB.1.MX', 'SITESB-1.MX')
    naftrac['Ticker'] = naftrac['Ticker'].replace('GFREGIOO.MX', 'RA.MX')
    
    # Convertir Fecha a datetime
    naftrac['Date'] = pd.to_datetime(naftrac['Date'],format='%Y%m%d')
    # Cambio de indice
    naftrac = naftrac.set_index("Date")
    return naftrac


# Función para eliminar activos
def conversion_cash(df): 
    # Cambiamos tickers a cash (KOFL.MX, KOFUBL.MX, USD.MXN, BSMXB.MX, NMKA.MX ) quitamos tambien MXN para poder usar en funcion de descarga de precios
    deltickers = ['MXN.MX','KOFL.MX', 'KOFUBL.MX', 'USD.MX', 'BSMXB.MX', 'NMKA.MX','NEMAKA.MX']
    df = df[~df['Ticker'].isin(deltickers)]

    return df


# Función para descargar precios (adj close)
def price_adj_close(tickers, start_date=None, end_date=None, freq=None):
    closes = pd.DataFrame(columns=tickers, index=web.YahooDailyReader(tickers[0], start=start_date, end=end_date
                                                                      , interval=freq).read().index)
    for i in tickers:
        df = web.YahooDailyReader(symbols=i, start=start_date, end=end_date, interval=freq).read()
        closes[i] = df['Adj Close']
    closes.index_name = 'Date'
    closes = closes.sort_index()
    return closes