
import logging
import os
from datetime import datetime


class Logger:

    _loggers = {}

    @staticmethod
    def get_logger(name: str = "Framework") -> logging.Logger:
        if name in Logger._loggers:
            return Logger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%H:%M:%S"
            )
            console_handler.setFormatter(console_format)

            logs_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "logs"
            )
            os.makedirs(logs_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(logs_dir, f"test_run_{today}.log")

            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)s():%(lineno)d | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_format)

            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        Logger._loggers[name] = logger
        return logger
