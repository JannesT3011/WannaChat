import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[39;20m"
    blue = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;91m"
    reset = "\x1b[0m"
    # lines: (Line %(lineno)d)
    # FYI: all arguments for logging if you want to restyle :)
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    format = "[%(asctime)s] %(name)s [%(levelname)s] - %(message)s"
    error_critical_format = "[%(asctime)s] %(levelname)s - %(pathname)s (Line %(lineno)d)\n[%(asctime)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + error_critical_format + reset,
        logging.CRITICAL: bold_red + error_critical_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(CustomFormatter())
    logger.addHandler(console)

    return logger