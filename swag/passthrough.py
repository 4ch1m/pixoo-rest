from base64 import b64encode
from PIL import Image


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
  "Command": "Device/SetMirrorMode",
  "Mode": 0
}""", "Set screen mirror mode. (mode: 0=disable, 1=enable)"

device_get_device_time = """{
  "Command": "Device/GetDeviceTime"
}""", "Get the device system time."

device_set_dis_temp_mode = """{
  "Command": "Device/SetDisTempMode",
  "Mode": 0
}""", "Set temperature mode. (mode: 0=Celcius, 1=Fahrenheit)"

device_set_time_24_flag = """{
  "Command": "Device/SetTime24Flag",
  "Mode": 0
}""", "Set hours display mode. (mode: 0=12 hours, 1=24 hours)"

device_set_high_light_mode = """{
  "Command": "Device/SetHighLightMode",
  "Mode": 0
}""", "Set screen high light mode. (mode: 0=close, 1=open)"

device_set_white_balance = """{
  "Command": "Device/SetWhiteBalance",
  "RValue": 100,
  "GValue": 100,
  "BValue": 100
}""", "Set screen 'white balance'."

device_get_weather_info = """{
  "Command": "Device/GetWeatherInfo"
}""", "Get weather information."

device_play_buzzer = """{
  "Command": "Device/PlayBuzzer",
  "ActiveTimeInCycle": 500,
  "OffTimeInCycle": 500,
  "PlayTotalTime": 3000
}""", "Play the buzzer. (Parameter times are milliseconds.)"

tools_set_timer = """{
  "Command": "Tools/SetTimer",
  "Minute": 1,
  "Second": 0,
  "Status": 1
}""", "Control the timer. (status: 1=start, 0=stop)"

tools_set_stop_watch = """{
  "Command": "Tools/SetStopWatch",
  "Status": 1
}""", "Control the stopwatch. (status: 2=reset, 1=start, 0=stop)"

tools_set_score_board = """{
  "Command": "Tools/SetScoreBoard",
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
  "PicData": "{ b64encode(Image.open('swag/duck.gif').convert("RGB").tobytes()).decode("utf-8") }"
}}""", "Send animation to device. (NOTE: Multiple requests/objects need to be sent in sequence in order to create an animation; 'PicOffset' must be incremented (starting with 0); 'PicNum' must match the total number of GIFs.)"

draw_clear_http_text = """{
  "Command": "Draw/ClearHttpText"
}""", "Clear all text."

draw_reset_http_gif_id = """{
  "Command": "Draw/ResetHttpGifId"
}""", "Reset GIF id."

draw_send_http_item_list = """{
  "Command": "Draw/SendHttpItemList",
  "ItemList": [
    {
       "TextId": 5,
       "type": 6,
       "x": 32,
       "y": 32,
       "dir": 0,
       "font": 18,
       "TextWidth": 32,
       "Textheight": 16,
       "speed": 100,
       "align": 1,
       "color": "#FF0000"
    },
    {
       "TextId": 1,
       "type": 14,
       "x": 0,
       "y": 0,
       "dir": 0,
       "font": 18,
       "TextWidth": 32,
       "Textheight": 16,
       "speed": 100,
       "align": 1,
       "color": "#FF0000"
    },
    {
       "TextId": 2,
       "type": 22,
       "x": 16,
       "y": 16,
       "dir": 0,
       "font": 2,
       "TextWidth": 48,
       "Textheight": 16,
       "speed": 100,
       "align": 1,
       "TextString": "hello, divoom",
       "color": "#FFFFFF"
    },
    {
       "TextId": 20,
       "type": 23,
       "x": 0,
       "y": 48,
       "dir": 0,
       "font": 4,
       "TextWidth": 64,
       "Textheight": 16,
       "speed": 100,
       "update_time": 60,
       "align": 1,
       "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
       "color": "#FFF000"
    }
  ]
}""", "Draws (multiple) basic text elements at once. The elements include (scrolling) date, time and temperature strings."
