from pydantic import Field

from .common import (
    XYModel,
    RGBModel,
    TextWidthModel,
    ScrollSpeedModel,
    ScrollDirectionModel,
    AnimationSpeedModel,
    SkipFirstFrameModel
)


class GIFModel(AnimationSpeedModel, SkipFirstFrameModel):
    ...


class TextModel(XYModel, RGBModel, TextWidthModel, ScrollSpeedModel, ScrollDirectionModel):
    text: str = Field(min_length=1, max_length=511, default='Hello Pixoo!', description='The text to display.')
    identifier: int = Field(ge=0, le=19, default=0, description='The text identifier.')
    font: int = Field(ge=1, le=7, default=1, description='The font number.')
