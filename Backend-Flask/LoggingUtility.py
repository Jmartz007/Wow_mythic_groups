import logging
import logging.handlers
import os
import datetime
from logging.config import dictConfig

if not os.path.exists("logs"):
    os.makedirs("logs", exist_ok=True)
    print("Folder 'logs' created.")


def flip_name(log_path):
    """flips the file name of a log file to put the date in front"""
    log_dir, log_filename = os.path.split(log_path)
    file_name, ext, timestamp = log_filename.rsplit(".", 2)
    return os.path.join(log_dir, f"{file_name}.{timestamp}.{ext}")


# logging.handlers.TimedRotatingFileHandler()

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": 0,
        "formatters": {
            "std": {
                "format": "%(process)d %(processName)s [%(levelname)-5s] [%(module)s]: %(message)s"
            },
            "stdtime": {
                "format": "%(asctime)s [%(levelname)-5s] [%(module)s]: %(message)s",
                "datefmt": "%b-%d-%y %I:%M:%S %p",
            },
        },
        "handlers": {
            "console": {
                "formatter": "std",
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            },
            "file": {
                "formatter": "stdtime",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "filename": "logs/WoWapp.log",
                "when": "W1",
                "atTime": datetime.time(8, 0),
                # "interval": 7,
                "backupCount": 8,
                ".": {"namer": flip_name},
            },
            "fileerrors": {
                "formatter": "stdtime",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "WARNING",
                "filename": "logs/WoWapp-Errors.log",
                "when": "W1",
                "atTime": datetime.time(8, 0),
                # "interval": 7,
                "backupCount": 8,
                ".": {"namer": flip_name},
            },
        },
        "loggers": {
            "main": {"handlers": ["console", "file", "fileerrors"], "level": "DEBUG"},
        },
    }
)
