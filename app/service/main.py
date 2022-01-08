from app.service.context import ApplicationContext
from app.service.settings import Settings
from fractal import Fractal


class ApplicationFractal(Fractal):
    settings = Settings()
    context = ApplicationContext()
