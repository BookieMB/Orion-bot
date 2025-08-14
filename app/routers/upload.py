from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io

router = APIRouter()

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
        width, height = img.size
        return {
            "filename": file.filename,
            "format": img.format,
            "width": width,
            "height": height
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")
