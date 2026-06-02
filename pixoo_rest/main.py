import sys
import time

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from pixoo_rest import helpers
from pixoo_rest.api_tags import APITags
from pixoo_rest.settings import Settings
from pixoo_rest.models.response import ResponseModel

from pixoo_rest.routers import (
    set_router,
    draw_router,
    send_router,
    download_router,
    divoom_router,
    passthrough_router
)


settings = Settings.get()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    if settings.pixoo_connection_check:
        for connection_test_count in range(settings.pixoo_connection_check_retries + 1):
            if helpers.try_to_request(f'http://{settings.pixoo_host}/get'):
                break

            if connection_test_count == settings.pixoo_connection_check_retries:
                sys.exit(f'Failed to connect to [{settings.pixoo_host}]. Exiting.')
            else:
                time.sleep(30)

    yield
    ...  # no shutdown tasks atm


app = FastAPI(
    title='Pixoo REST',
    version=(Path(__file__).parent.parent / Path('version.txt')).read_text(),
    description='A RESTful API to easily interact with the Wi-Fi enabled {} devices.'.format(
        '<a href="https://www.divoom.com/de/products/pixoo-64">Divoom Pixoo</a>'
    ),
    terms_of_service='',
    contact={
        'name': '4ch1m / GitHub',
        'url': 'https://github.com/4ch1m/pixoo-rest'
    },
    base_path=settings.pixoo_rest_root_path,
    url_prefix=settings.pixoo_rest_root_path,
    tags_metadata=[
        {
            'name': APITags.DRAW.value,
            'description': 'draw lines, pixels, rectangles, etc. on your Pixoo'
        },
        {
            'name': APITags.SEND.value,
            'description': 'send text, GIFs, etc. to your Pixoo'
        },
        {
            'name': APITags.SET.value,
            'description': 'set brightness, channel, clock, etc. on your Pixoo'
        },
        {
            'name': APITags.PASSTHROUGH.value,
            'description': "directly pass commands to your Pixoo's built-in HTTP-API"
        },
        {
            'name': APITags.DIVOOM.value,
            'description': f'send requests to the external vendor API ({settings.divoom_api_url})'
        },
        {
            'name': APITags.DOWNLOAD.value,
            'description': 'automatically download and send resources to your Pixoo'
        }
    ],
    root_path=settings.pixoo_rest_root_path,
    debug=settings.pixoo_rest_debug,
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)


STATIC_RESOURCE_PATH = Path(__file__).parent.parent / Path('static')


@app.get('/', include_in_schema=False)
async def home(request: Request) -> RedirectResponse:
    return RedirectResponse(f'{request.base_url}docs')


@app.get('/favicon.ico', include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(STATIC_RESOURCE_PATH / Path('favico.icon'))


@app.get('/static/{sub_path}', include_in_schema=False)
async def static_file(sub_path: str) -> FileResponse:
    return FileResponse(STATIC_RESOURCE_PATH / Path(sub_path))


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=f'{settings.pixoo_rest_root_path}{app.openapi_url}',
        title=f'{app.title} - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url=f'{settings.pixoo_rest_root_path}/static/favicon.ico',
        swagger_js_url=f'{settings.pixoo_rest_root_path}/static/swagger-ui-bundle.js',
        swagger_css_url=f'{settings.pixoo_rest_root_path}/static/swagger-ui.css'
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    return get_swagger_ui_oauth2_redirect_html()


@app.get('/redoc', include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    return get_redoc_html(
        openapi_url=f'{settings.pixoo_rest_root_path}{app.openapi_url}',
        title=f'{app.title} - ReDoc',
        redoc_favicon_url=f'{settings.pixoo_rest_root_path}/static/favicon.ico',
        redoc_js_url=f'{settings.pixoo_rest_root_path}/static/redoc.standalone.js'
    )


@app.get('/health', response_model=ResponseModel)
async def health() -> ResponseModel:
    return ResponseModel(message='OK')


for router in [
    set_router,
    draw_router,
    send_router,
    download_router,
    divoom_router,
    passthrough_router
]:
    app.include_router(router)
