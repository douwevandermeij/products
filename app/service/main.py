from fractal import Fractal

from app.service.context import ApplicationContext
from app.service.settings import Settings


class ProductFractal(Fractal):
    settings = Settings()
    context = ApplicationContext()
