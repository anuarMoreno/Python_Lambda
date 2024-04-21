import unittest
from unittest.mock import patch, MagicMock
import mainFunction
import json

class TestLambdaFunction(unittest.TestCase):
    @patch('mainFunction.obtener_precio_crypto')
    @patch('mainFunction.escribir_en_dynamodb')
    def test_lambda_handler(self, mock_escribir_en_dynamodb, mock_obtener_precio_crypto):
        # Simulamos la respuesta de obtener_precio_crypto
        mock_obtener_precio_crypto.return_value = (12345.67, 23456.78, '2022-01-01T00:00:00.000Z', 0)
        
        # Simulamos la respuesta de escribir_en_dynamodb
        mock_escribir_en_dynamodb.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        
        # Llamamos a la función lambda_handler con un evento y contexto ficticios
        result = mainFunction.lambda_handler({}, None)
        
        # Verificamos que la función devolvió el resultado esperado
        self.assertEqual(result, {'statusCode': 200, 'body': json.dumps('Elemento escrito en la tabla de DynamoDB')})
        
        # Verificamos que las funciones mockeadas se llamaron correctamente
        mock_obtener_precio_crypto.assert_called_once()
        mock_escribir_en_dynamodb.assert_called_once()

if __name__ == '__main__':
    unittest.main()