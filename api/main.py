
from typing import Union

from fastapi import FastAPI

from spreader.packages import up_package, down_package, get_packages

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/spreader/up/{package}')
def spreader_up(package: str):
    up_package(package_name=package)
    return {"package": package, "status": "up"}


@app.get('/spreader/down/{package}')
def spreader_down(package: str):
    down_package(package_name=package)
    return {"package": package, "status": "down"}


@app.get('/spreader/list')
def spreader_list():
    packages = get_packages()
    return packages


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
