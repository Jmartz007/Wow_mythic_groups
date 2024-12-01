class ServiceException(Exception):
    """Custom Base class for service-layer exceptions."""

    pass


class DatabaseError(ServiceException):
    """Custom exception raised for database related errors."""

    def __init__(self, message="An error occurred in the database"):
        super().__init__(message)
