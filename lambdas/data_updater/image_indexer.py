import json
import os
import boto3


class ImageIndexer:
    def handler(self, payload: dict) -> dict:
        try:
            product_id = self.get_product_id(payload)
            product_img_url = self.get_public_img_url(payload)

            product = self.update_product(product_id, product_img_url)

            return {"statusCode": 200, "body": json.dumps(product)}
        except Exception as e:
            print(e)

            return {"statusCode": 500, "body": "Internal server error"}

    # Get product id from s3 event body
    def get_product_id(self, payload: dict) -> str:
        try:
            object_name = payload["s3"]["object"]["key"]
            product_id, file_extension = os.path.splitext(os.path.basename(object_name))

            return product_id
        except Exception as e:
            raise e

    # Get public url for product image
    def get_public_img_url(self, payload: dict) -> str:
        try:
            s3_bucket_name = "product-catalog-aws-workshop-1"
            bucket_location = boto3.client("s3").get_bucket_location(
                Bucket=s3_bucket_name
            )
            object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
                bucket_location["LocationConstraint"],
                s3_bucket_name,
                payload["s3"]["object"]["key"],
            )
            return object_url
        except Exception as e:
            raise e

    def update_product(self, product_id: str, img_url: str) -> dict:
        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table("ProductCatalogue")

            response = table.update_item(
                Key={"id": product_id},
                UpdateExpression="set has_image = :val1, img_url = :val2",
                ExpressionAttributeValues={":val1": True, ":val2": img_url},
                ReturnValues="UPDATED_NEW",
            )

            return response
        except Exception as e:
            raise e


def lambda_handler(event, context):
    image_indexer = ImageIndexer()
    return image_indexer.handler(event["Records"][0])
