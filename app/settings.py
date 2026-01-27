from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DB_USER: str
    DB_PASSWORD: str
    DB_HOSTPORT: str
    DB_CONTAINER_PORT: int
    DB_ECHO: bool
    DB_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    DEBUG: bool

    @classmethod
    def from_env(cls) -> "Settings":
        echo = getenv("DB_ECHO")
        if echo not in ["true", "false"]:
            raise ValueError(
                "DB_ECHO environment variable must be either 'true' or 'false'"
            )
        DB_ECHO = True if echo == "true" else False

        debug = getenv("DEBUG")
        if debug not in ["true", "false"]:
            raise ValueError(
                "DEBUG environment variable must be either 'true' or 'false'"
            )
        DEBUG = True if debug == "true" else False

        DB_USER=getenv("DB_USER")
        DB_PASSWORD=getenv("DB_PASSWORD")
        DB_HOSTPORT=getenv("DB_HOSTPORT")
        DB_CONTAINER_PORT=int(getenv("DB_CONTAINER_PORT"))
        JWT_SECRET=getenv("JWT_SECRET")
        JWT_ALGORITHM=getenv("JWT_ALGORITHM")
        DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@localhost:{DB_HOSTPORT}/{DB_USER}"


        return cls(
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWORD,
            DB_HOSTPORT=DB_HOSTPORT,
            DB_CONTAINER_PORT=DB_CONTAINER_PORT,
            DB_ECHO=DB_ECHO,
            DB_URL=DB_URL,
            JWT_SECRET=JWT_SECRET,
            JWT_ALGORITHM=JWT_ALGORITHM,
            DEBUG=DEBUG,
        )


settings = Settings.from_env()
