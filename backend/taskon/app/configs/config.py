from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str = "postgresql+psycopg://taskon_admin:adm@127.0.0.1:15432/taskon_db"
    cors_allow_origins: list[str] = field(default_factory=lambda: ["http://localhost:3000"])
    cors_allow_methods: list[str] = field(default_factory=lambda: ["*"])
