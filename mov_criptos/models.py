import sqlite3
import requests #forcoinAPI
from config import *
from mov_criptos.connection import Connection
from mov_criptos.forms import RegistrosForm


def show_all():
    connect = Connection("SELECT id,date,time,moneda_from,cantidad_from,moneda_to,cantidad_to,precio_unitario from registros order by date DESC, time DESC")
    filas = connect.res.fetchall()
    columnas= connect.res.description

    resultado =[]
   
    for fila in filas:
        dato={}
        posicion=0

        for campo in columnas:
            dato[campo[0]]=fila[posicion]
            posicion += 1
        resultado.append(dato)

    connect.con.close()

    return resultado

def save(registro):
    connect = Connection(f"INSERT INTO registros (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, precio_unitario) VALUES(?,?,?,?,?,?,?)", registro)
    connect.con.commit()
    connect.con.close()  

def eurosSpent():
    connect = Connection(f"SELECT sum(cantidad_from) FROM Registros WHERE moneda_from = 'EUR'")
    resultado = connect.res.fetchall()
    connect.con.close()
    resultado = f'{resultado[0][0]:,.2f}'
    resultado = resultado.replace(',', '*')
    resultado = resultado.replace('.', ',')
    resultado = resultado.replace('*', '.')
    return resultado

def eurosSpentRaw():
    connect = Connection(f"SELECT sum(cantidad_from) FROM Registros WHERE moneda_from = 'EUR'")
    resultado = connect.res.fetchall()
    connect.con.close()
    return resultado[0][0]

def eurosGained():
    connect = Connection(f"SELECT sum(cantidad_to) FROM Registros WHERE moneda_to = 'EUR'")
    resultado = connect.res.fetchall()
    connect.con.close()
    resultado = f'{resultado[0][0]:,.2f}'
    resultado = resultado.replace(',', '*')
    resultado = resultado.replace('.', ',')
    resultado = resultado.replace('*', '.')
    return resultado    

def eurosGainedRaw():
    connect = Connection(f"SELECT sum(cantidad_to) FROM Registros WHERE moneda_to = 'EUR'")
    resultado = connect.res.fetchall()
    connect.con.close()
    return resultado[0][0]

def formatQuantity(quantity):
    if quantity >=1:
        resultado = f'{quantity:,.2f}'
        resultado = resultado.replace(',', '*')
        resultado = resultado.replace('.', ',')
        resultado = resultado.replace('*', '.')
    else:
        resultado = f'{quantity:,.6f}'
        resultado = resultado.replace(',', '*')
        resultado = resultado.replace('.', ',')
        resultado = resultado.replace('*', '.')

    return resultado

class ModelError(Exception):
    pass

class CryptoExchange:
    def __init__(self, moneda_from, moneda_to):
        self.moneda_from = moneda_from
        self.moneda_to = moneda_to
        self.rate = 0

    def getRate(self):
        r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{self.moneda_from}/{self.moneda_to}?apikey={API_KEY}')
        resultado = r.json()
        if r.status_code == 200:
            self.rate = resultado['rate']
            
            return self.rate

        else:
            raise ModelError(f"status: {self.r.status_code} error: {self.resultado['error']}")
