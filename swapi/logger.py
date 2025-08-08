import logging

import colorlog


def get_logger(name: str = __name__, debug: bool = False) -> logging.Logger:
    """
    Create and configure a colorized logger.

    :param name: Logger name, defaults to __name__
    :param debug: Enable debug level logging, defaults to False
    :return: Configured logger with colored output
    :rtype: logging.Logger
    """
    level = logging.DEBUG if debug else logging.INFO

    # Create a colored formatter
    formatter = colorlog.ColoredFormatter(
        "%(asctime)s [%(log_color)s%(levelname)s%(reset)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear previous handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    if debug:
        logger.debug("Debug mode is ON")

    return logger

    return logger
