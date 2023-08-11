from fastapi import UploadFile, HTTPException
from io import BytesIO
import pandas as pd
from moto import mock_s3
import boto3
import uuid
import requests
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
bucket_name = os.getenv("DEST_BUCKET")



async def filecsv_to_dict(file: UploadFile):
    filename = file.filename
    extention = filename.split(".")[-1]
    if extention != "csv" and extention != "CSV":
        return "error"
    csv_content = await file.read()
    csv_io = BytesIO(csv_content)
    df = pd.read_csv(csv_io)
    df['count'] = df['count'].astype('Int64', errors='ignore')
    result_dict = df.to_dict("records")
    return result_dict


def upload_to_s3(data: dict):
    with mock_s3():
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket=bucket_name)

        response = requests.get(data["url"])
        image_bytesio = BytesIO(response.content)

        bucket = conn.Bucket(bucket_name)
        bucket.upload_fileobj(image_bytesio, "test")
        id_image = uuid.uuid4()
    print(f"image saved in route: s3://{bucket_name}/{id_image}/{data['date']}/{data['url'].split('/')[-1]}")


def fetch_images(elem: dict):
    params = {key:value for key, value in elem.items() if not pd.isna(value)}
    params["api_key"]= api_key
    response = requests.get(url=base_url,params=params).json()

    if isinstance(response, list):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(upload_to_s3, i) for i in response]
    else:
        upload_to_s3(response)