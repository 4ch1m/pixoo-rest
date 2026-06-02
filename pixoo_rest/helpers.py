import json
import base64
import logging

from functools import lru_cache

import requests

from PIL import ImageFile

from .settings import Settings
from .pixoo.src.pixoo.objects.pixoo import Pixoo


logger = logging.getLogger(__name__)


@lru_cache()
def get_pixoo() -> Pixoo:
    settings = Settings.get()

    return Pixoo(
        settings.pixoo_host,
        settings.pixoo_screen_size,
        settings.pixoo_debug
    )


def try_to_request(url: str) -> bool:
    logger.info(f'initiating request to "{url}"')

    result = requests.get(url).status_code == 200

    if result:
        logger.info(f'request to "{url}" succeeded')
    else:
        logger.error(f'request to "{url}" failed')

    return result


def handle_gif(gif: ImageFile.ImageFile, speed: int, skip_first_frame: bool) -> None:
    pixoo = get_pixoo()

    if gif.is_animated:
        requests.post(f'http://{pixoo.ip_address}/post', json.dumps({
            'Command': 'Draw/ResetHttpGifId'
        }))

        gif_frames = []

        for i in range((1 if skip_first_frame else 0), gif.n_frames):
            if len(gif_frames) == 59:
                break

            gif.seek(i)

            if gif.size not in ((16, 16), (32, 32), (64, 64)):
                gif_frames.append(gif.resize((pixoo.size, pixoo.size)).convert('RGB'))
            else:
                gif_frames.append(gif.convert('RGB'))

        for offset, gif_frame in enumerate(gif_frames):
            requests.post(f'http://{pixoo.ip_address}/post', json.dumps({
                'Command': 'Draw/SendHttpGif',
                'PicID': 1,
                'PicNum': len(gif_frames),
                'PicOffset': offset,
                'PicWidth': gif_frame.width,
                'PicSpeed': speed,
                'PicData': base64.b64encode(gif_frame.tobytes()).decode('utf-8')
            }))
    else:
        pixoo.draw_image(gif)
        pixoo.push()
