#!/usr/bin/env python3

"""Returns random open restaurants or other locations from Google Maps"""

import json
import sys
import traceback
from typing import Union
from time import sleep
from random import shuffle
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import googlemaps
import googlemaps.geocoding
import googlemaps.places

__version__ = "1.2.1"


def _get_random_items(items: list, number: int = None) -> list:
    """
    Get random items from a list of items

    :param items: A list of items
    :param number: The number of items to return
    :return: A list of random items
    """
    if number is not None:
        if number > len(items):
            number = len(items)
    _items = items.copy()
    shuffle(_items)

    return _items[:number]


def _bool_filter(items: list[dict], key: str) -> list:
    """
    Filter a list of dictionaries based on boolean values.
    dictionaries that do not contain a matching key
    with a value of True are filtered out.

    :param items: A list of dictionaries
    :param key: The dictionary key containing a boolean value
    :return: A filtered list of dictionaries
    """
    def _check_value(x: dict):
        if key not in x:
            return False
        return x[key] is True
    filtered_items = items.copy()
    filtered_items = filter(_check_value, filtered_items)

    return list(filtered_items)


def find_open_places(gmaps: googlemaps.Client,
                     keyword: str, near: Union[str, tuple, dict], radius=8046,
                     details: bool = False,
                     filters: list[str] = None) -> list[dict]:
    """
    Find open Places on Google Maps

    :param gmaps: A Google Maps Platform client
    :param keyword: Search terms
    :param near: A location (e.g., city or address) or a (lat,lng) tuple/dict
    :param radius: A radius in meters
    :param details: Include place details
    :param filters: A list of boolean keys to filter by
    :return: A list of places
    """
    if filters is None:
        filters = []
    if type(near) is str:
        location = googlemaps.geocoding.geocode(gmaps, address=near)
        location = location[0]["geometry"]["location"]
    elif type(near) is tuple or type(near) is list:
        location = dict(lat=float(near[0]), lng=float(near[1]))
    else:
        location = near
    response = googlemaps.places.places_nearby(gmaps,
                                               keyword=keyword,
                                               open_now=True,
                                               location=location,
                                               radius=radius)
    results = response["results"]
    if "next_page_token" in response:
        sleep(2)
        response = googlemaps.places.places_nearby(
            gmaps,
            page_token=response["next_page_token"])
        results += response["results"]
        if len(filters) or details:
            for i in range(len(results)):
                results[i] = get_place_details(gmaps, results[i]["place_id"])
        if len(filters):
            for key in filters:
                results = _bool_filter(results, key)

    return results


def get_place_details(gmaps: googlemaps.Client,
                      place: Union[str, dict]) -> dict:
    """
    Get details of a Place on Google Maps

    :param gmaps: A Google Maps Platform client
    :param place: A Google Maps Place ID or dictionary
    :return: Place details
    """
    if type(place) is str:
        return googlemaps.places.place(gmaps,
                                       place_id=place)["result"]
    elif "formatted_address" in place:
        return place
    return googlemaps.places.place(gmaps,
                                   place_id=place["place_id"])["result"]


def get_random_open_places(gmaps: googlemaps.Client,
                           keyword: str, near: Union[str, tuple, dict],
                           radius=8046,
                           details: bool = False,
                           filters: list[str] = None,
                           max_results: int = None) -> list[dict]:
    """
    Find random open Places on Google Maps

    :param gmaps: A Google Maps Platform client
    :param keyword: Search terms
    :param near: A location (e.g., city or address) or a (lat,lng) tuple/dict
    :param radius: A radius in meters
    :param details: Include place details
    :param filters: A list of boolean keys to filter by
    :param max_results: The maximum number of results to return
    :return: A list of places
    """
    places = find_open_places(gmaps, keyword, near,
                              radius=radius, filters=filters)
    random_places = _get_random_items(places, max_results)
    if details:
        for i in range(len(random_places)):
            random_places[i] = get_place_details(gmaps, random_places[i])

    return random_places


def _main():
    args = ArgumentParser(description=__doc__,
                          formatter_class=ArgumentDefaultsHelpFormatter)
    args.add_argument("location",
                      help="the geographic location to search")
    args.add_argument("--version",
                      action="version", version=__version__)
    args.add_argument("--debug", action="store_true",
                      help="print exception stacktraces")
    args.add_argument("--config", "-c", default="config.json",
                      help="the path to the configuration file")
    args.add_argument("--radius", "-r", type=int,
                      help="the radius of the search area in meters",
                      default=8046)
    args.add_argument("-n", type=int, default=1,
                      help="the maximum number of results to return")
    args.add_argument("--keyword", "-k", default="Restaurant",
                      help="the keyword to search for "
                      "(use quotes around multiple keywords)")
    args.add_argument("--delivery", "-d", action="store_true",
                      help="only return locations that offer delivery")
    args.add_argument("--takeout", "-t", action="store_true",
                      help="only return locations that offer takeout")
    args.add_argument("--wheelchair", "-w", action="store_true",
                      help="only return locations that have a " 
                      "wheelchair-accessible entrance")
    args.add_argument("--json", "-j", action="store_true",
                      help="output in JSON format")
    args = args.parse_args()

    filters = []

    try:
        with open(args.config) as config_file:
            config = json.loads(config_file.read())
        key = config["key"]
        gmaps = googlemaps.Client(key=key)
        if args.delivery:
            filters.append("delivery")
        if args.takeout:
            filters.append("takeout")
        if args.wheelchair:
            filters.append("wheelchair_accessible entrance")
        random_places = get_random_open_places(gmaps,
                                               keyword=args.keyword,
                                               near=args.location,
                                               radius=args.radius,
                                               details=True,
                                               filters=filters,
                                               max_results=args.n)
        if args.json:
            print(json.dumps(random_places, indent=2))
            exit()
        for place in random_places:
            print(f'{place["name"]}')
            print(f'{place["formatted_address"]}')
            if "formatted_phone_number" in place:
                print(f'{place["formatted_phone_number"]}')
            print(f'{place["url"]}')
            print()
    except Exception as e:
        if args.debug:
            print(traceback.format_exc())
        else:
            print(e, file=sys.stderr)
        exit(-1)


if __name__ == "__main__":
    _main()
