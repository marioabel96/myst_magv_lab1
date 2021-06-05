# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 1: Inversión de Capital                                                        -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: marioabel96                                                                                 -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/marioabel96/myst_magv_lab1                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #

import numpy as np
import pandas as pd
import datetime

def get_dates(list_of_files):
    dates = [i.strftime('%Y-%m-%d') for i in sorted([pd.to_datetime(i[8:]).date() for i in list_of_files])]
    return dates


def df_act_prices(naftrac_stats, monthly_closes, dates):
# Acomodamos el precio de cierre del activo en df de los  stats de naftrac
    mezcla = {}
    for date in dates:
        mezcla[date] = naftrac_stats[naftrac_stats.index == date].reset_index().set_index('Ticker').T

    for date in dates:
        mezcla[date].loc['Close'] = 0
        for ticker in monthly_closes.columns:
            mezcla[date].loc['Close'][ticker] = monthly_closes.loc[date][ticker]
            mezcla[date].columns.sort_values()

    mezcla_lt = [v for k, v in mezcla.items()]
    final = pd.concat(mezcla_lt, axis=1)
    final = final.T
    final = final.reset_index()
    
    return final


def inv_pasiva_posicion(df_stats, date, capital, comision):
    #Función que calculara el valor del portafolio en la fecha inicial


    # Obtenemos un df con la fecha donde se inicializa el portfalio
    Pesos_df = df_stats.loc[df_stats['Date'] == date]

    # Numero de acciones de acuerdo al capital, recordando que no hay pedazos de acciones usamos floor
    Pesos_df['Acciones'] = np.floor((capital*Pesos_df['Peso (%)'])/Pesos_df['Close'])

    # Valor de la posición
    Pesos_df['$ Total'] = Pesos_df['Acciones']*Pesos_df['Close']

    # Comision x accion ($)
    Pesos_df['Comisión'] = Pesos_df['$ Total']*comision

    return Pesos_df


def pasive_invstmnt_rend(portafolio_pasivo, lapso, capital, naftrac_stats):

    # Calculamos comision y cash
    total_comision = portafolio_pasivo['Comisión'].sum()
    cash = (1 - portafolio_pasivo['Peso (%)'].sum())*capital

    # df_pasiva

    # Tomamos stats de solo esas fechas
    n_s_pandemia = naftrac_stats.loc[naftrac_stats['Date'].isin(lapso)]

    ## eliminamos los pesos
    del n_s_pandemia['Peso (%)']

    # Anexamos el # de acciones * activo
    prueba = pd.merge(portafolio_pasivo,n_s_pandemia,on='Ticker' ,how='outer')
    del prueba['Date_x']
    del prueba['Peso (%)']
    del prueba['Close_x']
    del prueba['$ Total']
    del prueba['Comisión']

    # Calculamos el valor de las posiciones x mes
    prueba['Valor Posición'] = prueba['Acciones']*prueba['Close_y']
    pd.to_numeric(prueba['Valor Posición'])
    prueba = prueba.dropna()

    # Sumamos el valor total x mes de las posiciones
    prueba = prueba.set_index("Date_y")
    prueba = prueba.sort_index(ascending=True)
    prueba = prueba.resample('D').sum()
    prueba = prueba.loc[~(prueba==0).all(axis=1)]

    # Generamos una nueva columna con el total de la posición y añadimos cash - comision total
    prueba['capital'] = prueba['Valor Posición'] + cash - total_comision

    # Limpiamos el df prueba con solo las cols que necesitamos 
    del prueba['Ticker']
    del prueba['Acciones']
    del prueba['Close_y']
    del prueba['Valor Posición']

    # Añadimos el portafolio antes de las operaciones un dia anterior (2017-12-31, 1000000)
    #creamos df con valores iniciales
    ini = {'Date_y': [portafolio_pasivo.iloc[0,1]-datetime.timedelta(1)], 'capital': [capital]}
    ini = pd.DataFrame(ini)
    ini = ini.set_index('Date_y')

    # prueba con inicio en $1M (capital)
    prueba = ini.append(prueba)

    # Calculo de rendimientos logaritmicos
    prueba['rend'] =np.log(prueba/prueba.shift(1))
    prueba = prueba.fillna(0)

    # Calculo de rendimiento acumulado
    prueba['rend_acum'] = prueba['rend'].cumsum()
    prueba = prueba.fillna(0)

    #renombramos el indice como ejemplo lab
    prueba.index.names = ['timestamp']

    return prueba
