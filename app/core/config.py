from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornConfig(BaseModel):
    host: str
    port: int
    reload: bool


class Settings(BaseSettings):
    uc: UvicornConfig

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_prefix="APP_",
        env_nested_delimiter="_"
    )


settings = Settings()
