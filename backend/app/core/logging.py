import logging

import colorlog


def setup_logging():
    root_logger = logging.getLogger()

    # Don't add handlers if they already exist (prevents duplicate logs)
    if root_logger.handlers:
        return

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s:%(reset)s     [%(name)s] %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
