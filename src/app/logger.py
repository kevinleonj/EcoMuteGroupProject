import logging
import sys

logger = logging.getLogger("ecomute_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler("ecomute.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


# Dependency injection function — this is what Ex2 asks for
def get_logger() -> logging.Logger:
    return logger