from pydantic import Field

from .common import (
    TimeoutModel,
    SSLVerifyModel,
    AnimationSpeedModel,
    SkipFirstFrameModel,
    XYModel,
    ScrollDirectionModel,
    ScrollSpeedModel,
    PushImmediatelyModel,
    TextWidthModel,
    TextHeightModel,
    RGBModel,
    UserAgentModel
)


class GifModel(TimeoutModel, SSLVerifyModel, AnimationSpeedModel, SkipFirstFrameModel, UserAgentModel):
    url: str = Field(
        default='https://raw.githubusercontent.com/4ch1m/pixoo-rest/master/examples/duck.gif',
        description='The URL of the animated GIF image to be downloaded and then displayed. (Automatically gets resized.)'
    )


class ImageModel(TimeoutModel, SSLVerifyModel, XYModel, PushImmediatelyModel, UserAgentModel):
    url: str = Field(
        default='https://raw.githubusercontent.com/4ch1m/pixoo-rest/master/examples/Heart_pixelart.png',
        description='The URL of the image be downloaded and displayed. (Automatically gets resized.)'
    )


class TextModel(XYModel, ScrollDirectionModel, ScrollSpeedModel, TextWidthModel, TextHeightModel, RGBModel):
    id: int = Field(ge=0, le=39, default=1, description='Unique id of this text element.')
    url: str = Field(
        pattern=r'^(https:|http:|www\.)\S*',
        default='https://raw.githubusercontent.com/4ch1m/pixoo-rest/master/examples/text_download.json',
        description='The URL from which the text should be queried from.'
    )
    update_interval: int = Field(ge=1, default=60, description='Update interval in seconds.')
    horizontal_alignment: int = Field(ge=1, le=3, description='Horizontal alignment. (1 = left, 2 = middle, 3 = right)')
