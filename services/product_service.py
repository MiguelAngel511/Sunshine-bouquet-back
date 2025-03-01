import json
import os
from itertools import product
from typing import List

from fastapi import UploadFile
from starlette.responses import JSONResponse, FileResponse

from models.product import Product

DATA_FILE = "database/data.json"
IMAGES_FILE_PATH = "images"
def load_products()->List[Product]:
    ensure_database()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Product(**item) for item in data]
    return []

def ensure_database():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)


def save_data(data:Product):
    products=load_products()
    for i in products:
        if i.id==data.id:
            raise Exception("El id ingresado ya existe")
    ensure_database()
    products.append(data)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump([x.model_dump() for x in products], file, indent=4)

async def upload_product_image(file: UploadFile):
    os.makedirs(IMAGES_FILE_PATH, exist_ok=True)
    file_location = os.path.join(IMAGES_FILE_PATH, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"message": "Imagen subida con éxito", "filename": file.filename}

async def get_file(filename: str):
    file_path = os.path.join(IMAGES_FILE_PATH, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"message": "Imagen no encontrada"})
    return FileResponse(file_path)