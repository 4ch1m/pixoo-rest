# Changelog

## 1.3.0 (2023-01-06)

* new: 'divoom' section (query official [API](https://app.divoom-gz.com))
* dependency updates
* other minor improvements

## 1.2.0 (2022-10-29)

* new environment settings `PIXOO_REST_HOST` and `PIXOO_REST_DEBUG` (see [README](README.md))
* new passthrough-commands:
  * GetDeviceTime
  * SetDisTempMode
  * SetTime24Flag
  * setHighLightMode
  * SetWhiteBalance
  * GetWeatherInfo
  * PlayBuzzer
* other minor improvements

## 1.1.0 (2022-10-05)

* improved [Dockerfile](Dockerfile) (checkout of the pixoo-library's explicit commit-hash; which should correlate with the git-submodule and pin the actual dependencies)
* new `screen/on/{true|false}` endpoint
* new passthrough-commands:
  * SetScreenRotationAngle
  * SetMirrorMode
* other minor improvements

## 1.0.0 (2022-03-05)

* initial release