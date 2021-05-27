from sanic import Sanic
from sanic import app, response
from sanic.response import json, redirect, text
from pyArango.connection import *
from datetime import datetime
from datetime import timedelta
import json
import asyncio
import requests
import aiohttp
import simplejson
app = Sanic("My Hello, world app")


# VARIABLES DE CONEXIÓN CON ARANGODB!
con = Connection(arangoURL="http://arango.conoce360.tech", username="root",password="")
#con = Connection(arangoURL="http://localhost:8529/", username="root",password="")
bd = con["_system"]
# VARIABLES PARA EL DIA PYTHON
now = datetime.now()
new_date = now - timedelta(days=1)
hoy = str(now)
ayer = str(new_date)

# METODO GET
@app.route('/obtenerData', methods=['GET'])
async def estado(request):
    aql = 'For V1 in Sensors_Sensors return V1'
    queryResult = bd.AQLQuery(aql, rawResults = True, batchSize = 100)
    result = [V1 for V1 in queryResult]
    print("CONSULTA REALIZADA!")
    return response.json(result)

# METODO GET POR FECHA
@app.route('/obtenerDataFecha', methods=['GET'])
async def estado(request):
    now = datetime.now()
    new_date = now - timedelta(days=1)
    hoy = str(now)
    ayer = str(new_date)
    aql = 'For V1 in Sensors_Sensors filter V1.date >= "'+ayer+'" && V1.date <= "'+hoy+'" return V1'
    queryResult = bd.AQLQuery(aql, rawResults = True, batchSize = 100)
    result = [V1 for V1 in queryResult]
    print("CONSULTA REALIZADA!")
    return response.json(result)
# METODO GET , INGRESA FECHA EN LA URL Y RETORNA LOS VALORES DE LA BDD
@app.get("/obtenerDataFechas/<var1>/<var2>")
async def tag_handler(request, var1, var2):
    fecha1 = format(var1)
    fecha2 = format(var2)
    aql = 'For V1 in Sensors_Sensors filter V1.date == "'+fecha1+'" OR V1.date == "'+fecha2+'" return V1'
    queryResult = bd.AQLQuery(aql, rawResults = True, batchSize = 100)
    result = [V1 for V1 in queryResult]
    print("CONSULTA REALIZADA!")
    result = response.json(result)
    return (result)

if __name__ == '__main__':
    app.run()
