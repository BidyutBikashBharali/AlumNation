from pydantic import BaseSettings


class Settings(BaseSettings):
    
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str
    DATABASE_URL: str
    class Config:
        env_file = './.env'


settings = Settings()

