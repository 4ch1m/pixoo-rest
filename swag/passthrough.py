from pathlib import Path


def create(example, description):
    return {
       'description': description,
       'parameters': [
            {
                'name': 'request',
                'description': 'The request object in JSON format.',
                'in': 'body',
                'schema': {
                    'type': 'string',
                    'example': example
                }
            }
       ],
       'responses': {
            '200': {
                'description': 'OK'
            }
       },
       'tags': [
           'pass-through'
       ]
    }


channel_set_index = """{
  "Command": "Channel/SetIndex",
  "SelectIndex": 1
}""", "Select channel. (index: 0=Faces, 1=Cloud, 2=Visualizer, 3=Custom)"

channel_set_custom_page_index = """{
  "Command": "Channel/SetCustomPageIndex",
  "CustomPageIndex": 1
}""", "Select custom channel. (index: 0 to ２)"

channel_set_eq_position = """{
  "Command": "Channel/SetEqPosition",
  "EqPosition": 0
}""", "Select visualizer. (position: starts from 0)"

channel_cloud_index = """{
  "Command": "Channel/CloudIndex",
  "Index": 0
}""", "Select cloud channel. (index: 0=Recommend gallery, 1=Favourite, 2=Subscribe artist)"

channel_get_index = """{
  "Command": "Channel/GetIndex"
}""", "Get current channel."

channel_set_brightness = """{
  "Command": "Channel/SetBrightness",
  "Brightness": 100
}""", "Set brightness. (brightness: 0 to 100)"

channel_get_all_conf = """{
  "Command": "Channel/GetAllConf"
}""", "Get all configurations."

channel_on_off_screen = """{
  "Command": "Channel/OnOffScreen",
  "OnOff": 1
}""", "Switch screen on/off. (onOff: 1=on, 0=off)"

sys_log_and_lat = """{
  "Command": "Sys/LogAndLat",
  "Longitude": "30.29",
  "Latitude": "20.58"
}""", "Set coordinates for weather information. (requested from https://openweathermap.org/)"

sys_timezone = """{
  "Command": "Sys/TimeZone",
  "TimeZoneValue": "GMT-5"
}""", "Set time zone."

device_set_utc = """{
  "Command": "Device/SetUTC",
  "Utc": 1672416000
}""", "Set UTC."

device_set_screen_rotation_angle = """{
  "Command": "Device/SetScreenRotationAngle",
  "Mode": 0
}""", "Set screen rotation angle. (mode: 0=normal, 1=90°, 2=180°, 3=270°)"

device_set_mirror_mode = """{
  "Command":"Device/SetMirrorMode",
  "Mode": 0
}""", "Set screen mirror mode. (mode: 0=disable, 1=enable)"

tools_set_timer = """{
  "Command":"Tools/SetTimer",
  "Minute": 1,
  "Second": 0,
  "Status": 1
}""", "Control the timer. (status: 1=start, 0=stop)"

tools_set_stop_watch = """{
  "Command": "Tools/SetStopWatch",
  "Status": 1
}""", "Control the stopwatch. (status: 2=reset, 1=start, 0=stop)"

tools_set_score_board = """{
  "Command":"Tools/SetScoreBoard",
  "BlueScore": 100,
  "RedScore": 79
}""", "Control the score board. (score: 0 to 999)"

tools_set_noise_status = """{
  "Command": "Tools/SetNoiseStatus",
  "NoiseStatus": 1
}""", "Control the noise status. (status: 1=start, 0=stop)"

draw_send_http_text = """{
  "Command": "Draw/SendHttpText",
  "TextId": 4,
  "x": 0,
  "y": 40,
  "dir": 0,
  "font": 4,
  "TextWidth": 56,
  "speed": 10,
  "TextString": "hello, Divoom",
  "color": "#FFFF00",
  "align": 1
}""", "Send text to device. (NOTE: This one strangely only works when called directly after drawing a GIF (via SendHttpGif).)"

draw_send_http_gif = f"""{{
  "Command": "Draw/SendHttpGif",
  "PicNum": 1,
  "PicWidth": 64,
  "PicOffset": 0,
  "PicID": 1000,
  "PicSpeed": 100,
  "PicData": "{ Path('swag/pic_data.base64').read_text() }"
}}""", "Send animation to device. (NOTE: Multiple JSON objects can be sent at once here; 'PicOffset' should be incremented then; 'PicNum' should match the total number of GIFs.)"

draw_clear_http_text = """{
  "Command":"Draw/ClearHttpText"
}""", "Clear all text."

draw_reset_http_gif_id = """{
  "Command":"Draw/ResetHttpGifId"
}""", "Reset GIF id."
