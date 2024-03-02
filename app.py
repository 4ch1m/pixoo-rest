import os
import time
import requests
import json
import base64

from dotenv import load_dotenv
from flask import Flask, request, redirect
from flasgger import Swagger, swag_from
from pixoo.pixoo import Channel, Pixoo
from PIL import Image

from swag import definitions
from swag import passthrough

import _helpers

load_dotenv()

pixoo_host = os.environ.get('PIXOO_HOST', 'Pixoo64')
pixoo_screen = int(os.environ.get('PIXOO_SCREEN_SIZE', 64))
pixoo_debug = _helpers.parse_bool_value(os.environ.get('PIXOO_DEBUG', 'false'))

while not _helpers.try_to_request(f'http://{pixoo_host}/get'):
    time.sleep(30)

pixoo = Pixoo(
    pixoo_host,
    pixoo_screen,
    pixoo_debug
)

app = Flask(__name__)
app.config['SWAGGER'] = _helpers.get_swagger_config()

swagger = Swagger(app, template=_helpers.get_additional_swagger_template())
definitions.create(swagger)


def _push_immediately(_request):
    if _helpers.parse_bool_value(_request.form.get('push_immediately', default=True)):
        pixoo.push()


@app.route('/', methods=['GET'])
def home():
    return redirect('/apidocs')


@app.route('/brightness/<int:percentage>', methods=['PUT'])
@swag_from('swag/set/brightness.yml')
def brightness(percentage):
    pixoo.set_brightness(percentage)

    return 'OK'


@app.route('/channel/<int:number>', methods=['PUT'])
@app.route('/face/<int:number>', methods=['PUT'])
@app.route('/visualizer/<int:number>', methods=['PUT'])
@app.route('/clock/<int:number>', methods=['PUT'])
@swag_from('swag/set/generic_number.yml')
def generic_set_number(number):
    if request.path.startswith('/channel/'):
        pixoo.set_channel(Channel(number))
    elif request.path.startswith('/face/'):
        pixoo.set_face(number)
    elif request.path.startswith('/visualizer/'):
        pixoo.set_visualizer(number)
    elif request.path.startswith('/clock/'):
        pixoo.set_clock(number)

    return 'OK'


@app.route('/screen/on/<boolean>', methods=['PUT'])
@swag_from('swag/set/generic_boolean.yml')
def generic_set_boolean(boolean):
    if request.path.startswith('/screen/on/'):
        pixoo.set_screen(_helpers.parse_bool_value(boolean))

    return 'OK'


@app.route('/image', methods=['POST'])
@swag_from('swag/draw/image.yml')
def image():
    pixoo.draw_image_at_location(
        Image.open(request.files['image'].stream),
        int(request.form.get('x')),
        int(request.form.get('y'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/text', methods=['POST'])
@swag_from('swag/draw/text.yml')
def text():
    pixoo.draw_text_at_location_rgb(
        request.form.get('text'),
        int(request.form.get('x')),
        int(request.form.get('y')),
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/fill', methods=['POST'])
@swag_from('swag/draw/fill.yml')
def fill():
    pixoo.fill_rgb(
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/line', methods=['POST'])
@swag_from('swag/draw/line.yml')
def line():
    pixoo.draw_line_from_start_to_stop_rgb(
        int(request.form.get('start_x')),
        int(request.form.get('start_y')),
        int(request.form.get('stop_x')),
        int(request.form.get('stop_y')),
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/rectangle', methods=['POST'])
@swag_from('swag/draw/rectangle.yml')
def rectangle():
    pixoo.draw_filled_rectangle_from_top_left_to_bottom_right_rgb(
        int(request.form.get('top_left_x')),
        int(request.form.get('top_left_y')),
        int(request.form.get('bottom_right_x')),
        int(request.form.get('bottom_right_y')),
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/pixel', methods=['POST'])
@swag_from('swag/draw/pixel.yml')
def pixel():
    pixoo.draw_pixel_at_location_rgb(
        int(request.form.get('x')),
        int(request.form.get('y')),
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/character', methods=['POST'])
@swag_from('swag/draw/character.yml')
def character():
    pixoo.draw_character_at_location_rgb(
        request.form.get('character'),
        int(request.form.get('x')),
        int(request.form.get('y')),
        int(request.form.get('r')),
        int(request.form.get('g')),
        int(request.form.get('b'))
    )

    _push_immediately(request)

    return 'OK'


@app.route('/sendText', methods=['POST'])
@swag_from('swag/send/text.yml')
def send_text():
    pixoo.send_text(
        request.form.get('text'),
        (int(request.form.get('x')), int(request.form.get('y'))),
        (int(request.form.get('r')), int(request.form.get('g')), int(request.form.get('b'))),
        (int(request.form.get('identifier'))),
        (int(request.form.get('font'))),
        (int(request.form.get('width'))),
        (int(request.form.get('movement_speed'))),
        (int(request.form.get('direction')))
    )

    return 'OK'


def _reset_gif():
    return requests.post(f'http://{pixoo.address}/post', json.dumps({
        "Command": "Draw/ResetHttpGifId"
    })).json()


def _send_gif(num, offset, width, speed, data):
    return requests.post(f'http://{pixoo.address}/post', json.dumps({
        "Command": "Draw/SendHttpGif",
        "PicID": 1,
        "PicNum": num,
        "PicOffset": offset,
        "PicWidth": width,
        "PicSpeed": speed,
        "PicData": data
    })).json()


def _handle_gif(gif, speed, skip_first_frame):
    if gif.is_animated:
        _reset_gif()

        for i in range(1 if skip_first_frame else 0, gif.n_frames):
            gif.seek(i)

            if gif.size not in ((16, 16), (32, 32), (64, 64)):
                gif_frame = gif.resize((pixoo.size, pixoo.size)).convert("RGB")
            else:
                gif_frame = gif.convert("RGB")

            _send_gif(
                gif.n_frames + (-1 if skip_first_frame else 0),
                i + (-1 if skip_first_frame else 0),
                gif_frame.width,
                speed,
                base64.b64encode(gif_frame.tobytes()).decode("utf-8")
            )
    else:
        pixoo.draw_image(gif)
        pixoo.push()


@app.route('/sendGif', methods=['POST'])
@swag_from('swag/send/gif.yml')
def send_gif():
    _handle_gif(
        Image.open(request.files['gif'].stream),
        int(request.form.get('speed')),
        _helpers.parse_bool_value(request.form.get('skip_first_frame', default=False))
    )

    return 'OK'


@app.route('/download/gif', methods=['POST'])
@swag_from('swag/download/gif.yml')
def download_gif():
    try:
        response = requests.get(
            request.form.get('url'),
            stream=True,
            timeout=int(request.form.get('timeout')),
            verify=_helpers.parse_bool_value(request.form.get('ssl_verify', default=True))
        )

        response.raise_for_status()

        _handle_gif(
            Image.open(response.raw),
            int(request.form.get('speed')),
            _helpers.parse_bool_value(request.form.get('skip_first_frame', default=False))
        )
    except (requests.exceptions.RequestException, OSError, IOError) as e:
        return f'Error downloading the GIF: {e}', 400

    return 'OK'


@app.route('/download/image', methods=['POST'])
@swag_from('swag/download/image.yml')
def download_image():
    try:
        response = requests.get(
            request.form.get('url'),
            stream=True,
            timeout=int(request.form.get('timeout')),
            verify=_helpers.parse_bool_value(request.form.get('ssl_verify', default=True))
        )

        response.raise_for_status()

        pixoo.draw_image_at_location(
            Image.open(response.raw),
            int(request.form.get('x')),
            int(request.form.get('y'))
        )

        _push_immediately(request)
    except (requests.exceptions.RequestException, OSError, IOError) as e:
        return f'Error downloading the image: {e}', 400

    return 'OK'


passthrough_routes = {
    # channel ...
    '/passthrough/channel/setIndex': passthrough.create(*passthrough.channel_set_index),
    '/passthrough/channel/setCustomPageIndex': passthrough.create(*passthrough.channel_set_custom_page_index),
    '/passthrough/channel/setEqPosition': passthrough.create(*passthrough.channel_set_eq_position),
    '/passthrough/channel/cloudIndex': passthrough.create(*passthrough.channel_cloud_index),
    '/passthrough/channel/getIndex': passthrough.create(*passthrough.channel_get_index),
    '/passthrough/channel/setBrightness': passthrough.create(*passthrough.channel_set_brightness),
    '/passthrough/channel/getAllConf': passthrough.create(*passthrough.channel_get_all_conf),
    '/passthrough/channel/onOffScreen': passthrough.create(*passthrough.channel_on_off_screen),
    # sys ...
    '/passthrough/sys/logAndLat': passthrough.create(*passthrough.sys_log_and_lat),
    '/passthrough/sys/timeZone': passthrough.create(*passthrough.sys_timezone),
    # device ...
    '/passthrough/device/setUTC': passthrough.create(*passthrough.device_set_utc),
    '/passthrough/device/SetScreenRotationAngle': passthrough.create(*passthrough.device_set_screen_rotation_angle),
    '/passthrough/device/SetMirrorMode': passthrough.create(*passthrough.device_set_mirror_mode),
    '/passthrough/device/getDeviceTime': passthrough.create(*passthrough.device_get_device_time),
    '/passthrough/device/setDisTempMode': passthrough.create(*passthrough.device_set_dis_temp_mode),
    '/passthrough/device/setTime24Flag': passthrough.create(*passthrough.device_set_time_24_flag),
    '/passthrough/device/setHighLightMode': passthrough.create(*passthrough.device_set_high_light_mode),
    '/passthrough/device/setWhiteBalance': passthrough.create(*passthrough.device_set_white_balance),
    '/passthrough/device/getWeatherInfo': passthrough.create(*passthrough.device_get_weather_info),
    '/passthrough/device/playBuzzer': passthrough.create(*passthrough.device_play_buzzer),
    # tools ...
    '/passthrough/tools/setTimer': passthrough.create(*passthrough.tools_set_timer),
    '/passthrough/tools/setStopWatch': passthrough.create(*passthrough.tools_set_stop_watch),
    '/passthrough/tools/setScoreBoard': passthrough.create(*passthrough.tools_set_score_board),
    '/passthrough/tools/setNoiseStatus': passthrough.create(*passthrough.tools_set_noise_status),
    # draw ...
    '/passthrough/draw/sendHttpText': passthrough.create(*passthrough.draw_send_http_text),
    '/passthrough/draw/clearHttpText': passthrough.create(*passthrough.draw_clear_http_text),
    '/passthrough/draw/sendHttpGif': passthrough.create(*passthrough.draw_send_http_gif),
    '/passthrough/draw/resetHttpGifId': passthrough.create(*passthrough.draw_reset_http_gif_id),
}


def _passthrough_request(passthrough_request):
    return requests.post(f'http://{pixoo.address}/post', json.dumps(passthrough_request.json)).json()


for _route, _swag in passthrough_routes.items():
    exec(f"""
@app.route('{_route}', methods=['POST'], endpoint='{_route}')
@swag_from({_swag}, endpoint='{_route}')
def passthrough_{list(passthrough_routes.keys()).index(_route)}():
    return _passthrough_request(request)
        """)


@app.route('/divoom/device/lan', methods=['POST'])
@swag_from('swag/divoom/device/return_same_lan_device.yml')
def divoom_return_same_lan_device():
    return _helpers.divoom_api_call('Device/ReturnSameLANDevice').json()


@app.route('/divoom/channel/dial/types', methods=['POST'])
@swag_from('swag/divoom/channel/get_dial_type.yml')
def divoom_get_dial_type():
    return _helpers.divoom_api_call('Channel/GetDialType').json()


@app.route('/divoom/channel/dial/list', methods=['POST'])
@swag_from('swag/divoom/channel/get_dial_list.yml')
def divoom_get_dial_list():
    return _helpers.divoom_api_call(
        'Channel/GetDialList',
        {
            'DialType': request.form.get('dial_type', default='Game'),
            'Page': int(request.form.get('page_number', default='1'))
        }
    ).json()


if __name__ == '__main__':
    app.run(
        debug=_helpers.parse_bool_value(os.environ.get('PIXOO_REST_DEBUG', 'false')),
        host=os.environ.get('PIXOO_REST_HOST', '127.0.0.1'),
        port=os.environ.get('PIXOO_REST_PORT', '5100')
    )
