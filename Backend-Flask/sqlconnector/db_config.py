from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class DBConfig:
    user: str
    password: str
    database: str
    port: int = 3306
    instance_host: Optional[str] = None
    local_connection_ip: Optional[str] = None
    instance_connection_name: Optional[str] = None

    @classmethod
    def from_env(cls) -> "DBConfig":
        return cls(
            user=os.getenv("DB_USERNAME", ""),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", ""),
            port=int(os.getenv("DB_PORT", "3306")),
            instance_host=os.getenv("INSTANCE_HOST"),
            local_connection_ip=os.getenv("LOCAL_CONNECTION_IP"),
            instance_connection_name=os.getenv("INSTANCE_CONNECTION_NAME"),
        )

    def validate(self) -> None:
        if not self.user:
            raise ValueError("DB_USERNAME environment variable is not set")
        if not self.password:
            raise ValueError("DB_PASSWORD environment variable is not set")
        if not self.database:
            raise ValueError("DB_NAME environment variable is not set")
        modes = [
            bool(self.instance_host),
            bool(self.local_connection_ip),
            bool(self.instance_connection_name),
        ]
        if sum(modes) != 1:
            raise ValueError(
                "Exactly one of LOCAL_CONNECTION_IP, INSTANCE_HOST, or INSTANCE_CONNECTION_NAME must be set"
            )

    def chosen_mode(self) -> str:
        if self.instance_host:
            return "instance_host"
        elif self.instance_connection_name:
            return "instance_connection_name"
        elif self.local_connection_ip:
            return "local_connection_ip"
        else:
            return "none"
