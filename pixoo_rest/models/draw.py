from pydantic import Field

from .common import (
    XYModel,
    RGBModel,
    PushImmediatelyModel
)


class CharacterModel(XYModel, RGBModel, PushImmediatelyModel):
    character: str = Field(min_length=1, max_length=1, default='X', description='The character to display.')


class FillModel(RGBModel, PushImmediatelyModel):
    ...


class ImageModel(XYModel, PushImmediatelyModel):
    ...


class LineModel(RGBModel, PushImmediatelyModel):
    start_x: int = Field(ge=0, default=0, description='Horizontal pixel position to start with.')
    start_y: int = Field(ge=0, default=0, description='Vertical pixel position to start with.')
    stop_x: int = Field(ge=-1, default=0, description='Horizontal pixel position to end with.')
    stop_y: int = Field(ge=-1, default=0, description='Vertical pixel position to end with.')


class PixelModel(XYModel, RGBModel, PushImmediatelyModel):
    ...


class RectangleModel(RGBModel, PushImmediatelyModel):
    top_left_x: int = Field(ge=0, default=0, description='Horizontal pixel position of the top left corner.')
    top_left_y: int = Field(ge=0, default=0, description='Vertical pixel position of the top left corner.')
    bottom_right_x: int = Field(ge=0, default=0, description='Horizontal pixel position of the bottom right corner.')
    bottom_right_y: int = Field(ge=0, default=0, description='Vertical pixel position of the bottom right corner.')


class TextModel(XYModel, RGBModel, PushImmediatelyModel):
    text: str = Field(default='Hello Pixoo!', description='The text to display.')
