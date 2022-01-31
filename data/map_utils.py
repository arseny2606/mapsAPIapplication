from io import BytesIO

import pygame
import requests

from data.constants import search_key, geocoder_key


def get_map(params=None, map_type="map"):
    req = f"https://static-maps.yandex.ru/1.x/?l={map_type}"
    if params:
        req += "&" + params
    response = requests.get(req)
    if not response:
        pass
    return pygame.image.load(BytesIO(response.content))


def find(ll, spn, text):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": search_key,
        "text": text,
        "lang": "ru_RU",
        "ll": ll,
        "spn": spn,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    json_response = response.json()
    organizations = json_response["features"]
    return organizations


def get(address):
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": geocoder_key,
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]


def get_coords(address):
    toponym = get(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_spn(address):
    toponym = get(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]["Envelope"]
    x1, y1 = envelope["lowerCorner"].split(" ")
    x2, y2 = envelope["upperCorner"].split(" ")
    dx = abs(float(x1) - float(x2)) / 2
    dy = abs(float(y1) - float(y2)) / 2
    spn = f"{dx},{dy}"
    return ll, spn


def get_near(point, kind):
    ll = f"{point[0]},{point[1]}"
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": geocoder_key,
        "geocode": ll,
        "format": "json"}
    if kind:
        geocoder_params["kind"] = kind
    response = requests.get(geocoder_request, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["name"]
