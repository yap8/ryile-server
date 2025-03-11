from datetime import timedelta
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# конфиг для базы данных
class DatabaseConfig(BaseModel):
    database: str = "postgresql"
    driver: str = "asyncpg"
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    name: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f"{self.database}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class TokenSettings(BaseModel):
    algorithm: str = "HS256"
    key: str
    default_exp_delta: timedelta = timedelta(days=10)


class SecutirySettings(BaseModel):
    salt: str


class ImagesSettings(BaseModel):
    path: Path = Path("../images").resolve()


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="_",
        env_prefix="STORE_CONFIG_",
    )

    db: DatabaseConfig
    token: TokenSettings
    security: SecutirySettings
    image: ImagesSettings = ImagesSettings()


settings = GlobalSettings()  # type: ignore
