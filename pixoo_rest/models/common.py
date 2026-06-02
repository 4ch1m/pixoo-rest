from enum import Enum
from pydantic import BaseModel, Field


class XYModel(BaseModel):
    x: int = Field(ge=0, default=0, description='Horizontal pixel position.')
    y: int = Field(ge=0, default=0, description='Vertical pixel position.')


class RGBModel(BaseModel):
    r: int = Field(ge=0, le=255, default=255, description='RGB - Red color value.')
    g: int = Field(ge=0, le=255, default=255, description='RGB - Green color value.')
    b: int = Field(ge=0, le=255, default=255, description='RGB - Blue color value.')


class PushImmediatelyModel(BaseModel):
    push_immediately: bool = Field(default=True, description='Push draw buffer to the device immediately after this operation?')


class TimeoutModel(BaseModel):
    timeout: int = Field(ge=3, le=300, default=3, description='Connection timeout in seconds.')


class SSLVerifyModel(BaseModel):
    ssl_verify: bool = Field(default=True, description='Verify SSL certificates for HTTPS requests.')


class ScrollDirectionModel(BaseModel):
    class Direction(int, Enum):
        LEFT = 0
        RIGHT = 1

    scroll_direction: Direction = Field(default=Direction.LEFT, description='The scroll direction. (0 = left; 1 = right)')


class ScrollSpeedModel(BaseModel):
    scroll_speed: int = Field(default=100, description='The scroll speed in milliseconds.')


class TextWidthModel(BaseModel):
    text_width: int = Field(ge=1, le=64, default=64, description='Text width.')


class TextHeightModel(BaseModel):
    text_height: int = Field(ge=1, le=64, default=16, description='Text height.')


class AnimationSpeedModel(BaseModel):
    animation_speed: int = Field(ge=0, default=100, description='Animation speed (in milliseconds).')


class SkipFirstFrameModel(BaseModel):
    skip_first_frame: bool = Field(default=False, description='Workaround for resized GIF images. Might help if the animation looks "glitchy" due to a faulty converted background-frame (= first frame) in the original GIF.')


class UserAgentModel(BaseModel):
    user_agent: str = Field(default='Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0', description='The "User-Agent" string that will be used when making the request.')
