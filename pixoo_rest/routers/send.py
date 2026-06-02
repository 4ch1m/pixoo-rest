import io

from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile, Depends

from PIL import Image

from ..api_tags import APITags
from ..helpers import get_pixoo, handle_gif
from ..models.send import GIFModel, TextModel
from ..models.response import ResponseModel


router = APIRouter(tags=[APITags.SEND])
pixoo = get_pixoo()


@router.post('/sendText', description='NOTE: This way of sending text to the device seems unreliable atm. The "draw text" method is a better alternative.', response_model=ResponseModel)
async def send_text(text_model: Annotated[TextModel, Form()]) -> ResponseModel:
    pixoo.send_text(
        text_model.text,
        (text_model.x, text_model.y),
        (text_model.r, text_model.g, text_model.b),
        text_model.identifier,
        text_model.font,
        text_model.text_width,
        text_model.scroll_speed,
        text_model.scroll_direction.value
    )

    return ResponseModel(message='OK')


@router.post('/sendGif', description='NOTE: The GIF should have max 59 animation frames.', response_model=ResponseModel)
async def send_gif(gif_model: GIFModel = Depends(), gif_file: UploadFile = File(description='The animated GIF image to display. (Automatically gets resized.)')) -> ResponseModel:
    gif_data = await gif_file.read()

    handle_gif(
        gif=Image.open(io.BytesIO(gif_data)),
        speed=gif_model.animation_speed,
        skip_first_frame=gif_model.skip_first_frame
    )

    return ResponseModel(message='OK')
