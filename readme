## Carga de datos a la base de datos en Dynamo DB

Para ello se configura una función lambda la cual tiene en sus permisos el acceso necesario para escribir en la base de datos Dynamo DB.

1. `mainFunction.py`: Este archivo contiene tres funciones principales que utilizo para obtener los precios de Bitcoin y Ethereum de la API de CoinMarketCap, escribir estos precios en una tabla de DynamoDB y manejar la ejecución de estas funciones en un entorno de AWS Lambda.

Las dependencias que utilizo son:

- json: Para trabajar con datos en formato JSON.
- boto3: Para interactuar con los servicios de AWS, en este caso, DynamoDB.
- os: Para trabajar con variables de entorno.
- datetime y timezone: Para trabajar con fechas y horas.
- requests: Para hacer solicitudes HTTP.
- decimal: Para trabajar con números decimales.

Las funciones en este archivo son:

- `obtener_precio_crypto()`: Hago una solicitud GET a la API de CoinMarketCap para obtener los precios más recientes de Bitcoin y Ethereum en USD. Utilizo una sesión de requests para hacer la solicitud y paso los parámetros y encabezados necesarios. Luego, extraigo los precios y la fecha de la consulta de la respuesta JSON y los devuelvo.
- `escribir_en_dynamodb(bitcoin_price, ethereum_price, querydate)`: Esta función toma los precios de Bitcoin y Ethereum y la fecha de la consulta, y los escribe en una tabla de DynamoDB. Convierto la fecha de la consulta a un objeto datetime y luego a un timestamp de Unix. Luego, utilizo boto3 para escribir un nuevo elemento en la tabla de DynamoDB con estos datos.
- `lambda_handler(event, context)`: Esta es la función principal que se ejecuta cuando se invoca mi función Lambda. Llamo a obtener_precio_crypto() para obtener los precios de las criptomonedas. Si no hay errores, llamo a escribir_en_dynamodb() para escribir los precios en DynamoDB y devuelvo una respuesta con un código de estado 200. Si hay un error, devuelvo una respuesta con un código de estado 500.