import json

from typing import Annotated, Any

from fastapi import APIRouter, Form, Response, status

import requests

from PIL import Image

from ..api_tags import APITags
from ..models.response import ResponseModel
from ..models.download import GifModel, TextModel, ImageModel
from ..helpers import get_pixoo, handle_gif


router = APIRouter(tags=[APITags.DOWNLOAD])
pixoo = get_pixoo()


@router.post('/download/gif', description='NOTE: The GIF should have max 60 animation frames.', response_model=ResponseModel)
async def download_gif(gif_model: Annotated[GifModel, Form()], response: Response) -> ResponseModel:
    try:
        response = requests.get(
            url=gif_model.url,
            stream=True,
            timeout=gif_model.timeout,
            verify=gif_model.ssl_verify,
            headers={"User-Agent": gif_model.user_agent}
        )

        response.raise_for_status()
    except (requests.exceptions.RequestException, OSError, IOError) as e:
        response.status_code = status.HTTP_424_FAILED_DEPENDENCY
        return ResponseModel(message=f'Error downloading the GIF: {e}')

    handle_gif(
        gif=Image.open(response.raw),
        speed=gif_model.animation_speed,
        skip_first_frame=gif_model.skip_first_frame,
    )

    return ResponseModel(message='OK')


@router.post('/download/image', response_model=ResponseModel)
def download_image(image_model: Annotated[ImageModel, Form()], response: Response) -> ResponseModel:
    try:
        response = requests.get(
            url=image_model.url,
            stream=True,
            timeout=image_model.timeout,
            verify=image_model.ssl_verify,
            headers={"User-Agent": image_model.user_agent}
        )

        response.raise_for_status()
    except (requests.exceptions.RequestException, OSError, IOError) as e:
        response.status_code = status.HTTP_424_FAILED_DEPENDENCY
        return ResponseModel(message=f'Error downloading the image: {e}')

    pixoo.draw_image_at_location(
        Image.open(response.raw),
        image_model.x,
        image_model.y
    )

    if image_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/download/text', description='''
Periodically queries text from an URL and draws it on screen. The text will scroll if too large.<br>
<br>
The query-response must contain a JSON-payload with this structure:
<pre>{ "ReturnCode": 0, "ReturnMessage": "", "DispData": "Hello World!" }</pre>
The device's built-in method [draw/sendHttpItemList](#/pass-through/post_passthrough_draw_sendHttpItemList) is used for this feature. 
''')
def download_text(text_model: Annotated[TextModel, Form()]) -> Any:
    return requests.post(f'http://{pixoo.ip_address}/post', json.dumps({
        'Command': 'Draw/SendHttpItemList',
        'ItemList': [
            {
                'type': 23,
                'TextId': text_model.id,
                'TextString': text_model.url,
                'x': text_model.x,
                'y': text_model.y,
                'dir': text_model.scroll_direction,
                'font': 4,
                'TextWidth': text_model.text_width,
                'Textheight': text_model.text_height,
                'speed': text_model.scroll_speed,
                'update_time': text_model.update_interval,
                'align': text_model.horizontal_alignment,
                'color': f'#{text_model.r:02x}{text_model.g:02x}{text_model.b:02x}'
            }
        ]
    })).json()
