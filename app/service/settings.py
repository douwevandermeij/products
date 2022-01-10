import os

from fractal.core.utils.settings import Settings as BaseSettings


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
    APP_NAME = os.getenv("APP_NAME", "products")

    def load(self):
        self.WEBSITE_HOST = os.getenv("WEBSITE_HOST", "http://localhost:8000")
        self.ALLOW_ORIGINS = os.getenv(
            "ALLOW_ORIGINS", ",".join(["http://localhost", self.WEBSITE_HOST])
        )

        self.SECRET_KEY = os.getenv("SECRET_KEY", "")

        self.PRODUCT_REPOSITORY_BACKEND = os.getenv("PRODUCT_REPOSITORY_BACKEND", "")
        self.EVENT_STORE_BACKEND = os.getenv("EVENT_STORE_BACKEND", "")

        self.GCP_SERVICE_ACCOUNT_KEY = os.getenv("GCP_SERVICE_ACCOUNT_KEY", "")
