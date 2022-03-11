import os
import tempfile
import requests
import json

from distutils.util import strtobool
from dotenv import load_dotenv
from flask import Flask, request, redirect
from flasgger import Swagger, swag_from
from pixoo.pixoo import Channel, Pixoo
from PIL import Image

from swag import definitions
from swag import passthrough

load_dotenv()

pixoo_host = os.environ.get('PIXOO_HOST', 'Pixoo64')

pixoo = Pixoo(
    pixoo_host,
    int(os.environ.get('PIXOO_SCREEN_SIZE', 64)),
    True
)

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Pixoo REST',
    'version': '1.0.0',
    'description': 'A RESTful API to easily interact with the Wi-Fi enabled {} devices.'.format(
        '<a href="https://www.divoom.com/de/products/pixoo-64">Divoom Pixoo</a>'
    ),
    'termsOfService': ''
}

swagger = Swagger(app)
definitions.create(swagger)


def _push_immediately(_request):
    if strtobool(_request.form.get('push_immediately', default=True)):
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
    if request.path.startswith('/channel'):
        pixoo.set_channel(Channel(number))
    elif request.path.startswith('/face'):
        pixoo.set_face(number)
    elif request.path.startswith('/visualizer'):
        pixoo.set_visualizer(number)
    elif request.path.startswith('/clock'):
        pixoo.set_clock(number)

    return 'OK'


@app.route('/image', methods=['POST'])
@swag_from('swag/draw/image.yml')
def image():
    request_image = Image.open(request.files['image'].stream)

    with tempfile.NamedTemporaryFile() as tmp_file:
        request_image.save(tmp_file, request_image.format)
        pixoo.draw_image_at_location(
            tmp_file.name,
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
@swag_from('swag/send_text.yml')
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


if __name__ == '__main__':
    app.run()
