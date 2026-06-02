import io

from typing import Annotated
from fastapi import APIRouter, Form, File, UploadFile, Depends

from PIL import Image

from ..api_tags import APITags
from ..helpers import get_pixoo
from ..models.response import ResponseModel
from ..models.draw import (
    ImageModel,
    LineModel,
    FillModel,
    PixelModel,
    TextModel,
    RectangleModel,
    CharacterModel
)


router = APIRouter(tags=[APITags.DRAW])
pixoo = get_pixoo()


@router.post('/image', response_model=ResponseModel)
async def image(image_model: ImageModel = Depends(), image_file: UploadFile = File(description='The image to display. (Automatically gets resized.)')) -> ResponseModel:
    image_data = await image_file.read()

    pixoo.draw_image_at_location(
        Image.open(io.BytesIO(image_data)),
        image_model.x,
        image_model.y
    )

    if image_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/text', response_model=ResponseModel)
async def text(text_model: Annotated[TextModel, Form()]) -> ResponseModel:
    pixoo.draw_text_at_location_rgb(
        text_model.text,
        text_model.x,
        text_model.y,
        text_model.r,
        text_model.g,
        text_model.b
    )

    if text_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/fill', response_model=ResponseModel)
async def fill(fill_model: Annotated[FillModel, Form()]) -> ResponseModel:
    pixoo.fill_rgb(
            fill_model.r,
            fill_model.g,
            fill_model.b
        )

    if fill_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/line', response_model=ResponseModel)
async def line(line_model: Annotated[LineModel, Form()]) -> ResponseModel:
    pixoo.draw_line_from_start_to_stop_rgb(
            line_model.start_x,
            line_model.start_y,
            line_model.stop_x,
            line_model.stop_y,
            line_model.r,
            line_model.g,
            line_model.b
        )

    if line_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/rectangle', response_model=ResponseModel)
async def rectangle(rectangle_model: Annotated[RectangleModel, Form()]) -> ResponseModel:
    pixoo.draw_filled_rectangle_from_top_left_to_bottom_right_rgb(
            rectangle_model.top_left_x,
            rectangle_model.top_left_y,
            rectangle_model.bottom_right_x,
            rectangle_model.bottom_right_y,
            rectangle_model.r,
            rectangle_model.g,
            rectangle_model.b
        )

    if rectangle_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/pixel', response_model=ResponseModel)
async def pixel(pixel_model: Annotated[PixelModel, Form()]) -> ResponseModel:
    pixoo.draw_pixel_at_location_rgb(
        pixel_model.x,
        pixel_model.y,
        pixel_model.r,
        pixel_model.g,
        pixel_model.b
    )

    if pixel_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')


@router.post('/character', response_model=ResponseModel)
async def character(character_model: Annotated[CharacterModel, Form()]) -> ResponseModel:
    pixoo.draw_character_at_location_rgb(
            character_model.character,
            character_model.x,
            character_model.y,
            character_model.r,
            character_model.g,
            character_model.b
        )

    if character_model.push_immediately:
        pixoo.push()

    return ResponseModel(message='OK')
