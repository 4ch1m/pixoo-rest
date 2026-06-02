from fastapi import APIRouter, Path

from ..helpers import get_pixoo
from ..api_tags import APITags
from ..models.response import ResponseModel


router = APIRouter(tags=[APITags.SET])
pixoo = get_pixoo()


@router.put('/brightness/{percentage}', response_model=ResponseModel)
async def brightness(percentage: int = Path(ge=0, le=100, description='Percentage value of display brightness.')) -> ResponseModel:
    pixoo.set_brightness(percentage)
    return ResponseModel(message='OK')


@router.put('/channel/{number}', response_model=ResponseModel)
async def channel(number: int = Path(ge=0, description='Channel number.')) -> ResponseModel:
    pixoo.set_channel(number)
    return ResponseModel(message='OK')


@router.put('/face/{number}', response_model=ResponseModel)
async def face(number: int = Path(ge=0, description='Face number.')) -> ResponseModel:
    pixoo.set_face(number)
    return ResponseModel(message='OK')


@router.put('/visualizer/{number}', response_model=ResponseModel)
async def visualizer(number: int = Path(ge=0, description='Visualizer number.')) -> ResponseModel:
    pixoo.set_visualizer(number)
    return ResponseModel(message='OK')


@router.put('/clock/{number}', response_model=ResponseModel)
async def clock(number: int = Path(ge=0, description='Clock number.')) -> ResponseModel:
    pixoo.set_clock(number)
    return ResponseModel(message='OK')


@router.put('/screen/on/{boolean}', response_model=ResponseModel)
async def screen_on(boolean: bool = Path(description='Screen on.')) -> ResponseModel:
    pixoo.set_screen(boolean)
    return ResponseModel(message='OK')
