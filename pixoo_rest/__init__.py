import logging
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(name)s) %(asctime)s | %(message)s',
    stream=sys.stdout
)

from .main import app
