from fastapi import APIRouter, UploadFile, File, HTTPException
import concurrent.futures
from typing import Dict

from routers.utils import fetch_images, filecsv_to_dict

router = APIRouter(prefix="/APOD_images", tags=["APOD"])

@router.post("/")
async def post_images_s3(file: UploadFile = File(...)) -> Dict:
    result_dict = await filecsv_to_dict(file)
    if isinstance(result_dict, str):
        raise HTTPException(status_code=400, detail="File is not a csv file")
    resp = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(fetch_images, result_dict))
            resp.extend(results)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error in a query: " + str(e))
    flat_list = [item for sublist in resp for item in sublist]
    return {"total_images_saved": len(flat_list), "data": flat_list}
