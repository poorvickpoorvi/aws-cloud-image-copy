# AWS Cloud Image Copy

## Project Overview
This project automatically copies images uploaded to one S3 bucket to another using AWS Lambda.

## AWS Services Used
- **S3**: Stores source and destination images.
- **Lambda**: Executes the function to copy images.
- **IAM**: Grants necessary permissions.
- **API Gateway** (optional): If extending functionality via API calls.

## Steps to Set Up the Project

### 1. Create S3 Buckets
- Go to AWS S3 Console.
- Create **two** buckets with unique names:
  - Source Bucket: `source-bucket-poorvick-12345`
  - Destination Bucket: `destination-bucket-poorvick-12345`

### 2. Create an IAM Role
- Go to AWS IAM Console.
- Create a new role with **AWS Lambda** as the trusted entity.
- Attach the following policy:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": [
    "arn:aws:s3:::source-bucket-poorvick-12345/*",
    "arn:aws:s3:::destination-bucket-poorvick-12345/*"
  ]
}
```

### 3. Deploy the Lambda Function
- Go to AWS Lambda Console.
- Click **Create function** > **Author from Scratch**.
- Set function name as `S3CopyFunction`.
- Select Python 3.x as runtime.
- Assign the IAM role created in Step 2.
- Paste the following code into the function:

```python
import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    destination_bucket = os.environ['DEST_BUCKET']
    
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        copy_source = {'Bucket': source_bucket, 'Key': object_key}
        s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=object_key)
    
    return {'statusCode': 200, 'body': 'Image copied successfully'}
```

### 4. Add Environment Variables
- Go to **Configuration > Environment Variables**.
- Add:
  - Key: `DEST_BUCKET`
  - Value: `destination-bucket-poorvick-12345`

### 5. Set Up S3 Trigger
- Go to **Configuration > Triggers**.
- Click **Add trigger**.
- Select **S3**.
- Choose **source-bucket-poorvick-12345**.
- Set **Event Type** to `PUT` (for new file uploads).
- Click **Add**.

### 6. Test the Function
- Upload an image to `source-bucket-poorvick-12345`.
- Check `destination-bucket-poorvick-12345` to see if the image was copied.

---

## Repository Structure
```
aws-cloud-image-copy/
│── lambda_function.py  # Lambda function script
│── README.md           # Project documentation
│── iam-policy.json     # IAM policy JSON
```

## Next Steps
- Add logging to track copy operations.
- Extend functionality with API Gateway for manual triggers.
- Implement error handling for failed copies.

---
### Author
**Poorvick** 🚀

