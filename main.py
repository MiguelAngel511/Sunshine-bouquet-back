import os
from typing import Union

from fastapi import FastAPI, Body, UploadFile, File
from starlette.middleware.cors import CORSMiddleware

from models.product import Product
from services.product_service import load_products, save_data, get_file, upload_product_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/products")
def list_products():
    return load_products()

@app.post("/products")
def save_products(product: Product):
    return save_data(product)

@app.get("/products/images/{filename}")
async def get_image_controller(filename: str):
    return get_file(filename)

@app.post("/products/upload/")
async def upload_image(file: UploadFile = File(...)):
    return await upload_product_image(file)


