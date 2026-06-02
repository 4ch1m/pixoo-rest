import json

from pathlib import Path
from types import CoroutineType
from typing import Annotated, Any, Callable

from fastapi import APIRouter, Body

import requests


from ..api_tags import APITags
from ..helpers import get_pixoo
from ..models.passthrough import PassthroughModel


router = APIRouter(tags=[APITags.PASSTHROUGH])
pixoo = get_pixoo()


passthrough_routes = [
    PassthroughModel(
        route_path='/passthrough/channel/setIndex',
        payload_filename='channel_set_index.json',
        description='Select channel. (index: 0=Faces, 1=Cloud, 2=Visualizer, 3=Custom)'),
    PassthroughModel(
        route_path='/passthrough/channel/setCustomPageIndex',
        payload_filename='channel_set_custom_page_index.json',
        description='Select custom channel. (index: 0 to ２)'),
    PassthroughModel(
        route_path='/passthrough/channel/setEqPosition',
        payload_filename='channel_set_eq_position.json',
        description='Select visualizer. (position: starts from 0)'),
    PassthroughModel(
        route_path='/passthrough/channel/cloudIndex',
        payload_filename='channel_cloud_index.json',
        description='Select cloud channel. (index: 0=Recommend gallery, 1=Favourite, 2=Subscribe artist)'),
    PassthroughModel(
        route_path='/passthrough/channel/getIndex',
        payload_filename='channel_get_index.json',
        description='Get current channel.'),
    PassthroughModel(
        route_path='/passthrough/channel/setBrightness',
        payload_filename='channel_set_brightness.json',
        description='Set brightness. (brightness: 0 to 100)'),
    PassthroughModel(
        route_path='/passthrough/channel/getAllConf',
        payload_filename='channel_get_all_conf.json',
        description='Get all configurations.'),
    PassthroughModel(
        route_path='/passthrough/channel/onOffScreen',
        payload_filename='channel_on_off_screen.json',
        description='Switch screen on/off. (onOff: 1=on, 0=off)'),
    PassthroughModel(
        route_path='/passthrough/sys/logAndLat',
        payload_filename='sys_log_and_lat.json',
        description='Set coordinates for weather information. (requested from https://openweathermap.org/)'),
    PassthroughModel(
        route_path='/passthrough/sys/timeZone',
        payload_filename='sys_timezone.json',
        description='Set time zone.'),
    PassthroughModel(
        route_path='/passthrough/device/setUTC',
        payload_filename='device_set_utc.json',
        description='Set UTC.'),
    PassthroughModel(
        route_path='/passthrough/device/SetScreenRotationAngle',
        payload_filename='device_set_screen_rotation_angle.json',
        description='Set screen rotation angle. (mode: 0=normal, 1=90°, 2=180°, 3=270°)'),
    PassthroughModel(
        route_path='/passthrough/device/SetMirrorMode',
        payload_filename='device_set_mirror_mode.json',
        description='Set screen mirror mode. (mode: 0=disable, 1=enable)'),
    PassthroughModel(
        route_path='/passthrough/device/getDeviceTime',
        payload_filename='device_get_device_time.json',
        description='Get the device system time.'),
    PassthroughModel(
        route_path='/passthrough/device/setDisTempMode',
        payload_filename='device_set_dis_temp_mode.json',
        description='Set temperature mode. (mode: 0=Celcius, 1=Fahrenheit)'),
    PassthroughModel(
        route_path='/passthrough/device/setTime24Flag',
        payload_filename='device_set_time_24_flag.json',
        description='Set hours display mode. (mode: 0=12 hours, 1=24 hours)'),
    PassthroughModel(
        route_path='/passthrough/device/setHighLightMode',
        payload_filename='device_set_high_light_mode.json',
        description='Set screen high light mode. (mode: 0=close, 1=open)'),
    PassthroughModel(
        route_path='/passthrough/device/setWhiteBalance',
        payload_filename='device_set_white_balance.json',
        description='Set screen "white balance".'),
    PassthroughModel(
        route_path='/passthrough/device/getWeatherInfo',
        payload_filename='device_get_weather_info.json',
        description='Get weather information.'),
    PassthroughModel(
        route_path='/passthrough/device/playBuzzer',
        payload_filename='device_play_buzzer.json',
        description='Play the buzzer. (Parameter times are milliseconds.)'),
    PassthroughModel(
        route_path='/passthrough/tools/setTimer',
        payload_filename='tools_set_timer.json',
        description='Control the timer. (status: 1=start, 0=stop)'),
    PassthroughModel(
        route_path='/passthrough/tools/setStopWatch',
        payload_filename='tools_set_stop_watch.json',
        description='Control the stopwatch. (status: 2=reset, 1=start, 0=stop)'),
    PassthroughModel(
        route_path='/passthrough/tools/setScoreBoard',
        payload_filename='tools_set_score_board.json',
        description='Control the score board. (score: 0 to 999)'),
    PassthroughModel(
        route_path='/passthrough/tools/setNoiseStatus',
        payload_filename='tools_set_noise_status.json',
        description='Control the noise status. (status: 1=start, 0=stop)'),
    PassthroughModel(
        route_path='/passthrough/draw/sendHttpText',
        payload_filename='draw_send_http_text.json',
        description='Send text to device. (NOTE: This one strangely only works when called directly after drawing a GIF (via SendHttpGif).)'),
    PassthroughModel(
        route_path='/passthrough/draw/clearHttpText',
        payload_filename='draw_clear_http_text.json',
        description='Clear all text.'),
    PassthroughModel(
        route_path='/passthrough/draw/sendHttpGif',
        payload_filename='draw_send_http_gif.json',
        description='Send animation to device. (NOTE: Multiple requests/objects need to be sent in sequence in order to create an animation; "PicOffset" must be incremented (starting with 0); "PicNum" must match the total number of GIFs.)'),
    PassthroughModel(
        route_path='/passthrough/draw/resetHttpGifId',
        payload_filename='draw_reset_http_gif_id.json',
        description='Reset GIF id.'),
    PassthroughModel(
        route_path='/passthrough/draw/sendHttpItemList',
        payload_filename='draw_send_http_item_list.json',
        description='Draws (multiple) basic text elements at once. The elements include (scrolling) date, time and temperature strings.')
]


def create_endpoint(passthrough_model: PassthroughModel) -> Callable[..., CoroutineType[Any, Any, Any]]:
    with open(Path(__file__).parent.parent / 'resources' / 'passthrough_payloads' / Path(passthrough_model.payload_filename), encoding='utf-8') as payload_file:
        payload = json.load(payload_file)

    async def endpoint(body: Annotated[dict, Body(examples=[payload], description=passthrough_model.description)]):
        return requests.post(url=f'http://{pixoo.ip_address}/post', json=body).json()

    return endpoint


for passthrough_route in passthrough_routes:
    router.add_api_route(
        name=passthrough_route.route_path.removeprefix('/passthrough/'),
        methods=['POST'],
        path=passthrough_route.route_path,
        description=passthrough_route.description,
        endpoint=create_endpoint(passthrough_route)
    )
