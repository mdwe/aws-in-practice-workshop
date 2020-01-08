import unittest
from unittest import mock
from lambdas.api.add_product import ProductHandler, validate_input, lambda_handler
from moto import mock_dynamodb2
import boto3
import json


def request_structure() -> dict:
    return {
        "name": "Funky Bear",
        "desc": "Money box Funky Bear 16x30 cm blue. Style: modern, vanguard. Material: dolomite",
    }


class TestAddProductHandler(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        boto3.setup_default_session(region_name="eu-central-1")

    # Test for add_product function with correct data
    @mock_dynamodb2
    def test_add_product_handler_add_product_with_correct_data(self):
        # DynamoDB mock
        table_name = "ProductCatalog"
        dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        request_body = request_structure()
        product_hanlder = ProductHandler(request_body["name"], request_body["desc"])
        product_hanlder.add_product()

        # validate product structure in DynamoDB
        db_response = table.get_item(Key={"id": product_hanlder.id})

        if "Item" in db_response:
            item = db_response["Item"]

        self.assertEqual(item["id"], product_hanlder.id)
        self.assertEqual(item["name"], request_body["name"])
        self.assertEqual(item["description"], request_body["desc"])

    # Test for add_product function with exception
    @mock_dynamodb2
    def test_add_product_handler_add_product_with_exception(self):
        request_body = request_structure()
        product_hanlder = ProductHandler(request_body["name"], request_body["desc"])
        self.assertRaises(Exception, product_hanlder.add_product)

    # Test for get_product function
    def test_add_product_handler_get_product(self):
        request_body = request_structure()
        product_handler = ProductHandler(request_body["name"], request_body["desc"])
        product = product_handler.get_product()

        self.assertTrue("id" in product)
        self.assertEqual(product["name"], request_body["name"])
        self.assertEqual(product["description"], request_body["desc"])

        product_handler.name = "Bear Funky"
        product = product_handler.get_product()
        self.assertEqual(product["name"], "Bear Funky")

    # Test for handler function with correct data
    @mock.patch.object(ProductHandler, "add_product")
    def test_add_product_handler_handler(self, add_product):
        request_body = request_structure()
        product_hanlder = ProductHandler(request_body["name"], request_body["desc"])
        response = product_hanlder.handler()

        # check api resposne structure
        self.assertEqual(response["statusCode"], 200)

        response_body = json.loads(response["body"])
        self.assertEqual(response_body["id"], product_hanlder.id)
        self.assertEqual(response_body["name"], request_body["name"])
        self.assertEqual(response_body["description"], request_body["desc"])

        # check api response if exception occured
        with mock.patch.object(ProductHandler, "add_product", side_effect=Exception()):
            response = product_hanlder.handler()

            # validate api resposne structure
            self.assertEqual(response["statusCode"], 500)
            self.assertEqual(response["body"], "Internal Server Error")


class TestAddProductLambda(unittest.TestCase):
    # Test for validate request body structure
    def test_add_product_lambda_validate_input(self):
        request_body = request_structure()
        self.assertTrue(validate_input(request_body))

        request_body = {}
        self.assertFalse(validate_input(request_body))

        request_body = {"name": "Test"}
        self.assertFalse(validate_input(request_body))

        request_body = {"desc": "Test"}
        self.assertFalse(validate_input(request_body))

    # Test for main lambda handler
    @mock.patch.object(ProductHandler, "handler", return_value={"statusCode": 200})
    def test_add_product_lambda_handler(self, mock_handler):
        response = lambda_handler({}, {})
        self.assertEqual(response["statusCode"], 400)

        request_body = request_structure()
        response = lambda_handler(request_body, {})
        self.assertEqual(response["statusCode"], 200)


if __name__ == "__main__":
    unittest.main()
