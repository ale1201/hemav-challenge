from fastapi import APIRouter, UploadFile, File, HTTPException
import concurrent.futures

from routers.utils import fetch_images, filecsv_to_dict

router = APIRouter(prefix="/APOD_images", tags=["APOD"])

@router.post("/")
async def post_images_s3(file: UploadFile = File(...)):
    result_dict = await filecsv_to_dict(file)
    if isinstance(result_dict, str):
        raise HTTPException(status_code=400, detail="File is not a csv file")
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(fetch_images, i) for i in result_dict]
    except Exception as e:
        raise HTTPException

    return {"message": "Hello World"}
