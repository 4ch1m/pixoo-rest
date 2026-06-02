# Changelog

## 2.0.0 (2026-06-02)

**___ MAJOR UPDATE ___**

* overall code rewrite due to migration from _Flask_ to [FastAPI](https://fastapi.tiangolo.com/)
* new:
  * [ReDoc](https://github.com/Redocly/redoc) integration
  * environment setting to disable initial connection check (`PIXOO_CONNECTION_CHECK`)
  * set custom user-agent string when using the download endpoints
* various other code improvements/optimizations
* updated dependencies

**IMPORTANT NOTE**:  
Several things regarding configuration have changed and need to be updated.  
The default port of _Pixoo REST_ has changed from `5000` to `8000` (in order to align with _FastAPI_'s default).  
Many environment variables (respectively their names) have also changed. Please (re-)check the [README](README.md) file and the [configuration section](https://github.com/4ch1m/pixoo-rest#configure) for details (e.g. `PIXOO_REST_ROOT_PATH` instead of `SCRIPT_PATH`, etc.).  
The actual API endpoints should (mostly) remain backwards compatible; but please check if your client calls still work as expected.

## 1.6.2 (2026-04-25)

* restructured code
* minor code improvements
* removal of `pixoo` PyPi-package usage; rollback to integration via git-submodule (see version `1.6.0`);  
the dependencies to `Flask`, `requests`, `pillow` and `python-dotenv` can now be controlled/updated independently again
* overall updated dependencies

## 1.6.1 (2025-12-18)

* dependency updates

## 1.6.0 (2024-08-28)

* removed `pixoo` as git-submodule; now added via PyPi package
* other dependencies updated

## 1.5.1 (2024-05-09)

* improved configuration options when running behind a reverse proxy:  
  the `SCRIPT_NAME` environment variable (see [WSGI docs](https://wsgi.readthedocs.io/en/latest/definitions.html#envvar-SCRIPT_NAME)) is now taken into consideration; making it possible to set a custom base-path

## 1.5.0 (2024-05-06)

* new:
  * (passthrough-)endpoint `sendHttpItemList`, which is available with the latest firmware update and offers drawing of multiple text-elements at once
  * custom `download/text` endpoint
  * Helm charts / K8s
* improved handling for GIF file upload (automatically limit to 59 frames; following the restriction of the device/API)
* updated dependencies
* other minor improvements

## 1.4.2 (2024-02-10)

* updated dependencies
* minor improvements (Dockerfile, docker-compose, log output, etc.)

## 1.4.1 (2023-10-16)

* updated dependencies
* minor improvements

## 1.4.0 (2023-07-23)

* new "download" endpoints (automatically download and send images to your Pixoo)

## 1.3.4 (2023-06-26)

* dependency updates

## 1.3.3 (2023-05-06)

* dependency updates

## 1.3.2 (2023-03-21)

* fix dependency conflict (`flasgger` requires `pillow` version `9.2.0`)

## 1.3.1 (2023-03-21)

* dependency updates
* "restart" directive removed from [docker-compose.yml](docker-compose.yml) 

## 1.3.0 (2023-01-06)

* new "divoom" section (= query official [API](https://app.divoom-gz.com))
* dependency updates
* other minor improvements

## 1.2.0 (2022-10-29)

* new environment settings `PIXOO_REST_HOST` and `PIXOO_REST_DEBUG` (see [README](README.md))
* new passthrough-commands:
  * `GetDeviceTime`
  * `SetDisTempMode`
  * `SetTime24Flag`
  * `setHighLightMode`
  * `SetWhiteBalance`
  * `GetWeatherInfo`
  * `PlayBuzzer`
* other minor improvements

## 1.1.0 (2022-10-05)

* improved [Dockerfile](Dockerfile) (checkout of the pixoo-library's explicit commit-hash; which should correlate with the git-submodule and pin the actual dependencies)
* new:
  * `screen/on/{true|false}` endpoint
  * passthrough-commands:
    * `SetScreenRotationAngle`
    * `SetMirrorMode`
* other minor improvements

## 1.0.0 (2022-03-05)

* initial release