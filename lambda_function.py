import boto3
import os

s3 = boto3.client("s3")
DEST_BUCKET = os.environ["DEST_BUCKET"]

def lambda_handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]

        copy_source = {"Bucket": source_bucket, "Key": object_key}
        
        try:
            s3.copy_object(
                Bucket=DEST_BUCKET,
                Key=object_key,
                CopySource=copy_source
            )
            print(f"Successfully copied {object_key} to {DEST_BUCKET}")
        except Exception as e:
            print(f"Error: {str(e)}")
            raise e
