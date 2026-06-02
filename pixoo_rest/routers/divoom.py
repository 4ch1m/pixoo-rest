from typing import Annotated, Any

import json

import requests
from requests import Response

from fastapi import APIRouter, Form

from ..settings import Settings
from ..api_tags import APITags
from ..models.divoom import DialListModel


router = APIRouter(tags=[APITags.DIVOOM])


def _divoom_api_call(endpoint: str, payload: dict | None = None) -> Response:
    return requests.post(
        f'{Settings.get().divoom_api_url}/{endpoint}',
        json.dumps(payload)
    )


@router.post('/divoom/device/lan', description='Get a list of all (Pixoo-)devices in your local network.')
def divoom_return_same_lan_device() -> Any:
    return _divoom_api_call('Device/ReturnSameLANDevice').json()


@router.post('/divoom/channel/dial/types', description='Get a list of all "dial" types.')
def divoom_get_dial_type() -> Any:
    return _divoom_api_call('Channel/GetDialType').json()


@router.post('/divoom/channel/dial/list', description='Get a list of all "dial" elements.')
def divoom_get_dial_list(dial_list_model: Annotated[DialListModel, Form()]) -> Any:
    return _divoom_api_call(
        'Channel/GetDialList',
        {
            'DialType': dial_list_model.dial_type,
            'Page': dial_list_model.page_number
        }
    ).json()
