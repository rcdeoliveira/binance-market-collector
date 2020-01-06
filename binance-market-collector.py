#!/usr/bin/env python3

import configparser
from binance.client import Client as BinanceClient
from binance.websockets import BinanceSocketManager
import influxdb


def writeToInflux(msg):
    fullQueryObject = jsonFromBinanceToInflux(msg, symbol)
    dbClient.write_points(fullQueryObject)


def jsonFromBinanceToInflux(binanceResponse, symbol):
    operations = ['bids', 'asks']
    operationsIndex = 0
    queryObject = []

    operationsIndex = 0
    while operationsIndex < len(operations):
        # binanceResponse has 3 elements, but the first doesn't matter
        binanceResponseIndex = 1

        while binanceResponseIndex < len(binanceResponse[operations[operationsIndex]]):
            operationObject = {}
            operationObject['measurement'] = symbol
            operationObject['tags'] = {"type": operations[operationsIndex]}
            operationObject['fields'] = {
                "price": binanceResponse[operations[operationsIndex]][binanceResponseIndex][0],
                "amount": binanceResponse[operations[operationsIndex]][binanceResponseIndex][1]
            }
            queryObject.append(operationObject)
            binanceResponseIndex += 1

        operationsIndex += 1

    return queryObject


# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')
apiKey = config['authentication']['apikey']
apiSecret = config['authentication']['apisecret']
symbol = config['symbol']['name']
depth = config['symbol']['depth']
dbHost = config['datastore']['dbhost']
dbName = config['datastore']['dbname']
dbPassword = config['datastore']['dbpassword']
dbPort = config['datastore']['dbport']
dbUser = config['datastore']['dbuser']

# connect to database
dbClient = influxdb.InfluxDBClient(
    host=dbHost,
    port=dbPort,
    username=dbUser,
    password=dbPassword,
    database=dbName)


# Create connection and websocket to Binance API
bnClient = BinanceClient(apiKey, apiSecret)
wsManager = BinanceSocketManager(bnClient)
connection = wsManager.start_depth_socket(
    symbol,
    writeToInflux,
    depth=depth)
wsManager.start()
