import json
import boto3
import urllib3


class ImageDownloader:
    def __init__(self, payload: dict):
        self.payload = payload

    def handler(self) -> dict:
        try:
            if not self.validate_msg():
                return {"statusCode": 400, "body": "Invalid message body"}

            msg = json.loads(self.payload["Sns"]["Message"])
            self.filename = msg["id"]
            self.img_url = msg["url"]

            self.download_image()

            return {
                "statusCode": 200,
                "body": "Image has been downloaded successfully!",
            }

        except Exception as e:
            raise e

    def validate_msg(self) -> bool:
        try:
            msg = json.loads(self.payload["Sns"]["Message"])
            return "id" in msg and "url" in msg
        except Exception:
            return False

    def download_image(self):
        try:
            # Get image data from external url and upload to S3
            http = urllib3.PoolManager()

            client = boto3.client("s3")
            image_data = http.request("GET", self.img_url, preload_content=False)
            image_data = image_data.data

            print(image_data)
            client.put_object(
                Body=http.request("GET", self.img_url, preload_content=False).data,
                Bucket="product-catalog-aws-workshop-1",
                Key=f"product-catalog/{self.filename}.jpg",
            )
        except Exception as e:
            print(e)
            raise e


def lambda_handler(event, context):
    print(event)

    image_downloader = ImageDownloader(event["Records"][0])
    return image_downloader.handler()
