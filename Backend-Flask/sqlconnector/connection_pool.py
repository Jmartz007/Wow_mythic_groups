# from __future__ import annotations
import os
import sqlalchemy

from .connect_connector import connect_with_connector
from .connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from .connect_tcp import connect_tcp_socket

from .connect_localconnection import local_conn
from sqlconnector.db_config import DBConfig


def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""

    cfg = DBConfig.from_env()
    cfg.validate()
    mode = cfg.chosen_mode()

    if mode == "instance_host":

        return connect_tcp_socket(cfg)

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if mode == "INSTANCE_CONNECTION_NAME":
        #     # Either a DB_USER or a DB_IAM_USER should be defined. If both are
        #     # defined, DB_IAM_USER takes precedence.
        return (
            connect_with_connector_auto_iam_authn(cfg)
            if os.environ.get("DB_IAM_USER")
            else connect_with_connector(cfg)
        )

    if mode == "local_connection_ip":
        return local_conn(cfg)

    raise ValueError(
        "Missing database connection type. Please define one of LOCAL_CONNECTION_IP,INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )


# Lazy-loaded engine for tests and runtime. Use `get_db()` to retrieve the
# engine; it will initialize on first call. Tests can inject an engine
# via `set_db()` to avoid real connections.

_DB_ENGINE: sqlalchemy.engine.base.Engine | None = None


def get_db() -> sqlalchemy.engine.base.Engine:
    """Return the global DB engine, initializing it on first use."""
    global _DB_ENGINE
    if _DB_ENGINE is None:
        _DB_ENGINE = init_connection_pool()
    return _DB_ENGINE


def set_db(engine: sqlalchemy.engine.base.Engine | None) -> None:
    """Set or clear the global DB engine. Tests can call `set_db(mock_engine)`
    to inject a test engine or `set_db(None)` to clear it.
    """
    global _DB_ENGINE
    _DB_ENGINE = engine
