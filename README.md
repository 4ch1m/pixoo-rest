# Pixoo REST

> A RESTful API to easily interact with the Wi-Fi enabled [Divoom Pixoo](https://www.divoom.com/de/products/pixoo-64) devices.

# Table of Contents

* [Introduction](#introduction)
* [Disclaimer](#disclaimer)
* [Getting started](#getting-started)
   * [Clone](#clone)
   * [Init](#init)
   * [Configure](#configure)
* [Running](#running)
   * [Direct](#direct)
   * [Containerized](#containerized)
* [Usage](#usage)
* [License](#license)

## Introduction

The main purpose of this app is to provide an easy-to-use [Swagger UI](https://swagger.io/tools/swagger-ui/) to interact with your Pixoo device.

Making it easier to ...

* :pencil2: **draw** pixels, lines, rectangles, and text
* :framed_picture: quickly **upload** images
* :gear: **set** the device's channel, brightness, etc.

... from your own applications or home-automation tasks.

**Pixoo REST** makes use of the great [Pixoo Python library](https://github.com/SomethingWithComputers/pixoo) by [SomethingWithComputers](https://github.com/SomethingWithComputers); which offers various helpful features like automatic image conversion. :thumbsup:

However, it is also possible to simply **pass through** raw JSON-data to the Pixoo's built-in HTTP-API via this Swagger UI.  
(The Swagger UI will provide handy example payloads (for easy editing) in this case.) 

## Disclaimer

This REST API is by no means a by-the-books reference on how proper REST APIs should be implemented; but simply a "convenience wrapper" for the aforementioned Pixoo library.

The actual HTTP API of the Pixoo device leaves a lot to be desired.  
First and foremost proper/official documentation. :wink:  
Most of the **pass-through** payload objects got discovered via *reverse engineering* or try-and-error.

:warning: Use at your own risk.

## Getting started

### Clone

Clone this repo ...
```bash
git clone https://github.com/4ch1m/pixoo-rest.git
```
... and change directory:
```bash
cd pixoo-rest
```

### Init

Initialize the _pixoo_ submodule:
```bash
git submodule init
git submodule update
```

### Configure

Create an `.env`-file alongside the [app.py](app.py)-file and put your individual settings in it; like so:
```properties
PIXOO_REST_PORT=5000
PIXOO_HOST=192.168.178.11
PIXOO_SCREEN_SIZE=64
```

## Running

The app can now be run ...
* :snake: directly; using your existing (venv-)Python installation

or

* :package: fully packaged inside a dedicated (Docker-)container

### Direct

Create a virtual environment and activate it (optional; but recommended):
```bash
python3 -m venv venv
. venv/bin/activate
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

Finally, run the app:
```bash
python app.py
```

### Containerized

Simply execute ...
```bash
docker-compose up
```
... to automatically build the container and run it.

## Usage

Open [http://localhost:5000](http://localhost:5000) in a web browser and make some requests using the [Swagger UI](https://swagger.io/):

![Screenshot](screenshot.png)

_NOTE:_  
For every executed request you'll get a handy [curl](https://curl.se/) command-line (ideal for reuse in home-automation scripts).

## License

Please read the [LICENSE](LICENSE) file.
