from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    NAME: str
    DRIVER: str = "postgresql+asyncpg"

    model_config = {"env_file": ".env"}

    @property
    def url(self) -> str:
        return f"{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.NAME}"


settings = Settings()
