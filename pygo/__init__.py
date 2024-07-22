# -*- coding: utf-8 -*-

import requests
from .api import APIImageLookUp,APILookUp
from .common import *
from .cache import Cache


checkUrl = requests.get(BASEURL)
if checkUrl.status_code() != 200:
    raise Exception(f"{checkUrl.status_code()}, Bad status code, API not reachable right now")

