class ServiceException(Exception):
    """Custom Base class for service-layer exceptions."""

    pass


class DatabaseError(ServiceException):
    """Custom exception raised for database related errors."""

    def __init__(self, message="An error occurred in the database"):
        super().__init__(message)


class DataNotFoundError(Exception):
    """Raised when the requested data cannot be found."""

    def __init__(self, message="No data found for the provided input", input=None):
        message = f"{message} {input}"
        super().__init__(message)


class PlayerNotFoundError(ServiceException):
    """Raised when a player cannot be found in the database"""

    def __init__(self, message="Player not found in database"):
        super().__init__(message)


class CharacterNotFoundError(ServiceException):
    """Raised when a character cannot be found in the database"""

    def __init__(self, message="Character not found in database"):
        super().__init__(message)
