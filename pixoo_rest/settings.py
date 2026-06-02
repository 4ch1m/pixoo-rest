import sys
import logging

from typing import Annotated
from functools import lru_cache

from pydantic import AfterValidator
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


def sanitize_root_path(root_path: str) -> str:
    return root_path.rstrip('/')


class Settings(BaseSettings, case_sensitive=False):
    pixoo_host: str = 'Pixoo64'
    pixoo_screen_size: int = 64
    pixoo_debug: bool = False
    pixoo_connection_check: bool = True
    pixoo_connection_check_retries: int = sys.maxsize
    pixoo_rest_debug: bool = False
    pixoo_rest_root_path: Annotated[str, AfterValidator(sanitize_root_path)] = ''
    divoom_api_url: str = 'https://app.divoom-gz.com'

    @staticmethod
    @lru_cache()
    def get() -> Settings:
        settings = Settings()
        logger.info(settings.model_dump_json(indent=4))

        return settings
