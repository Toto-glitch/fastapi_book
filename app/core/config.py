from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornConfig(BaseModel):
    host: str
    port: int
    reload: bool


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    echo: bool
    pool_size: int
    max_overflow: int

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    uc: UvicornConfig
    db: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__",
    )


settings = Settings()
