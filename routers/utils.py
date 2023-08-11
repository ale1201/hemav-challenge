from fastapi import UploadFile
from io import BytesIO
import pandas as pd
from moto import mock_s3
import boto3
import uuid
import requests
import concurrent.futures
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from typing import Dict, List, Any

load_dotenv()

api_key = os.getenv("API_KEY") 
base_url = os.getenv("BASE_URL")
bucket_name = os.getenv("DEST_BUCKET")


async def filecsv_to_dict(file: UploadFile) -> Dict | str:
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

def upload_to_s3(data: Dict) -> str | None:
    flag = True
    count_fails = 0
    while flag == True and count_fails <=5:
        with mock_s3():
            try: 
                conn = boto3.resource("s3", region_name="us-east-1")
                conn.create_bucket(Bucket=bucket_name)

                response = requests.get(data["url"])
                image_bytesio = BytesIO(response.content)

                bucket = conn.Bucket(bucket_name)
                bucket.upload_fileobj(image_bytesio, "test")
                id_image = uuid.uuid4()
                flag = False
                
                return f"image saved in route: s3://{bucket_name}/{id_image}/{data['date']}/{data['url'].split('/')[-1]}"
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucket':
                    print(f"Bucket '{bucket_name}' does not exist.")
                else:
                    # Handle other errors   
                    print(f"An error occurred: {e}")
                count_fails += 1
                print(count_fails)
            except Exception as e:
                print(f"An error occurred: {e}")
                count_fails += 1
                print(count_fails)

def fetch_images(elem: Dict) -> List | Any:
    flag = True
    count_fails = 0
    while flag == True and count_fails <=5:
        try:
            params = {key:value for key, value in elem.items() if not pd.isna(value)}
            params["api_key"]= api_key
            response = requests.get(url=base_url,params=params).json()
            resp = []
            if isinstance(response, list):
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    results = list(executor.map(upload_to_s3, response))
                    resp.extend(results)
            else:
                resp.extend([upload_to_s3(response)])
            flag = False
            return resp
        except Exception as e:
                if count_fails == 5:
                    if response:
                        raise Exception(response["msg"])
                    else:
                        raise Exception(f"An error occurred: {e}")
                if response:
                    print(response["msg"])
                else:
                    print(f"An error occurred: {e}")
                count_fails += 1
                print(count_fails)