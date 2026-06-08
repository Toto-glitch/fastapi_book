from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    uc: UvicornConfig = UvicornConfig()

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_prefix="APP_",
        env_nested_delimiter="_"
    )


settings = Settings()
