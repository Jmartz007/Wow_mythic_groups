# from __future__ import annotations
import os
import sqlalchemy

# from .connect_connector import connect_with_connector
# from .connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from .connect_tcp import connect_tcp_socket
from .connect_unix import connect_unix_socket
from .connect_localconnection import local_conn


def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""
    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    if os.environ.get("INSTANCE_HOST"):
        return connect_tcp_socket()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    # if os.environ.get("INSTANCE_CONNECTION_NAME"):
    #     # Either a DB_USER or a DB_IAM_USER should be defined. If both are
    #     # defined, DB_IAM_USER takes precedence.
    #     return (
    #         connect_with_connector_auto_iam_authn()
    #         if os.environ.get("DB_IAM_USER")
    #         else connect_with_connector()
    #     )

    if os.environ.get("LOCAL_CONNECTION_IP"):
        return local_conn()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
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
