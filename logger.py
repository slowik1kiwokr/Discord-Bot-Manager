import logging
from modules.config import LOG_DIR, LOG_FILE_PATH

# Gondoskodj róla, hogy a mappa létezzen (config.py már megteszi, de biztos ami biztos)
import os
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)