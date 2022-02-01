import math
from io import BytesIO

import pygame
import requests

from data import constants
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
        "type": "biz",
        "results": 1
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    json_response = response.json()
    try:
        organizations = json_response["features"][0]["properties"]["name"]
        category = json_response["features"][0]["properties"]["CompanyMetaData"]["Categories"][0]["name"]
        cords = json_response["features"][0]["geometry"]["coordinates"]
    except IndexError:
        return ""
    return organizations, category, cords


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
    try:
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]
        return features[0]["GeoObject"]
    except KeyError:
        return ""


def get_coords(address):
    toponym = get(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_spn(address):
    toponym = get(address)
    try:
        toponym_coodrinates = toponym["Point"]["pos"]
    except TypeError:
        return ""
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


def get_address(point):
    ll = f"{point[0]},{point[1]}"
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": geocoder_key,
        "geocode": ll,
        "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    json_response = response.json()
    try:
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]
        return features[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
    except IndexError:
        return ""


def screen_to_geo(self, pos):
    dy = 225 - pos[1]
    dx = pos[0] - 300
    lx = self.lon + dx * constants.coord_to_geo_x * math.pow(2, 15 - self.z)
    ly = self.lat + dy * constants.coord_to_geo_y * math.cos(math.radians(self.lat)) * \
         math.pow(2, 15 - self.z)
    return lx, ly


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance
