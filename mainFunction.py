import json
import boto3
import os
from datetime import datetime, timezone
from requests import Session
from decimal import Decimal

def obtener_precio_crypto():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

    parameters = {
        'id': '1,1027',
        'convert': 'USD'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('CMC_PRO_API_KEY'),
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    response_json = response.json()

    bitcoin_price = response_json['data']['1']['quote']['USD']['price']
    ethereum_price = response_json['data']['1027']['quote']['USD']['price']
    querydate = response_json['status']['timestamp']
    error_code = response_json['status']['error_code']
    
    print(f"Fecha de consulta: {querydate}")
    return bitcoin_price, ethereum_price, querydate, error_code


def escribir_en_dynamodb(bitcoin_price, ethereum_price, querydate):
    dynamodb = boto3.resource('dynamodb')
    tabla = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))
    
    # Convertir datequery a un objeto datetime
    querydate_datetime = datetime.strptime(querydate, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Convertir el objeto datetime a un timestamp de Unix
    timestamp = int(querydate_datetime.replace(tzinfo=timezone.utc).timestamp())
    
    respuesta = tabla.put_item(
       Item={
            'timestamp': timestamp,
            'precio_btc': Decimal(str(bitcoin_price)),  
            'precio_eth': Decimal(str(ethereum_price)),  
        }
    )
    print(f"Precios: BTC={bitcoin_price}, ETH={ethereum_price}, Timestamp={timestamp}")
    return respuesta


def lambda_handler(event, context):
    bitcoin_price, ethereum_price, querydate, error_code = obtener_precio_crypto()
    if error_code == 0:
        respuesta = escribir_en_dynamodb(bitcoin_price, ethereum_price, querydate)
        print('Ejecución correcta')
        return {
            'statusCode': 200,
            'body': json.dumps('Elemento escrito en la tabla de DynamoDB')
        }
    else:
        print('Error al obtener los precios de las criptomonedas')
        return {
            'statusCode': 500,
            'body': json.dumps('Error al obtener los precios de las criptomonedas')
        }

if __name__ == '__main__':
    os.environ['CMC_PRO_API_KEY'] = 'TU KEY'
    os.environ['DYNAMODB_TABLE_NAME'] = 'table-name'
    lambda_handler(None, None)