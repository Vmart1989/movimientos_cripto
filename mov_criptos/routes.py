from datetime import date, datetime
from mov_criptos import app
from flask import render_template, request, redirect, url_for, flash
from mov_criptos.models import *
from mov_criptos.forms import RegistrosForm

@app.route("/")
def index():
    registros = show_all()

    return render_template('index.html', pageTitle = 'Movimientos', data=registros )

@app.route("/purchase",methods=["GET","POST",])
def purchase():
    #global calcular_on

    if request.method == "GET":
        form = RegistrosForm()
        #calcular_on = False
        return render_template("purchase.html", pageTitle = "Transacción", dataForm = form)
    else: #POST
        form = RegistrosForm(data=request.form)
        moneda_from = form.moneda_from.data
        moneda_to = form.moneda_to.data
        cantidad = form.cantidad_from.data

        exchange = CryptoExchange(moneda_from, moneda_to)
        rate = exchange.getRate()
        cantidad_to = cantidad*rate
        precio_unitario = cantidad/cantidad_to

        cantidad_to_formatted = f'{cantidad_to:.6f}'
        rate_formatted = f'{rate:.6f}'
        p_u_formatted = f'{precio_unitario:.6f}'

        if form.calcular.data:
            #calcular_on = True
            return render_template("purchase.html",pageTitle = "Transacción en marcha", dataForm = form, rate=rate_formatted, cantidad_to=cantidad_to_formatted, precio_unitario = p_u_formatted, moneda_to=moneda_to, moneda_from=moneda_from, cantidad=cantidad)

        if form.submit.data:
            pass

@app.route("/status")
def status():
    return render_template("status.html", pageTitle = "Estado")