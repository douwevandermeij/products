from fractal.contrib.fastapi.install import install_fastapi
from fractal.contrib.fastapi.routers.default import inject_default_routes

from app.routers import products
from app.service.main import ProductFractal

fractal = ProductFractal()

app = install_fastapi(fractal.settings)

app.include_router(inject_default_routes(fractal.context), tags=["default"])

app.include_router(products.router, tags=["products"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
