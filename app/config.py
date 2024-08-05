from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_USER}"

    JWT_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file='.env')
    # for Pydantic v1
    # class Config:
    #     env_file = ".env"


settings = Settings()
