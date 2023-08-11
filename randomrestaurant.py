#!/usr/bin/env python3

import json
import sys
import traceback
from time import sleep
from random import shuffle
from argparse import ArgumentParser

import googlemaps
import googlemaps.geocoding
import googlemaps.places

"""Returns random restaurants or other locations from Google Maps"""

__version__ = "1.0.0"


def _get_random_items(items: list, number: int = None) -> list:
    if number is not None:
        if number > len(items):
            number = len(items)
        _items = items.copy()
        shuffle(_items)
    return _items[:number]


def get_places(gmaps: googlemaps.Client, keyword: str, near: str, radius=8046) -> list[dict]:
    location = googlemaps.geocoding.geocode(gmaps, address=near)
    location = location[0]["geometry"]["location"]
    response = googlemaps.places.places_nearby(gmaps,
                                               keyword=keyword,
                                               open_now=True,
                                               location=location,
                                               radius=radius)
    results = response["results"]
    if "next_page_token" in response:
        sleep(2)
        response = googlemaps.places.places_nearby(gmaps,
                                                   page_token=response["next_page_token"])
        results += response["results"]

    return results


def get_place_details(gmaps: googlemaps.Client, place_id: str) -> dict:
    return googlemaps.places.place(gmaps, place_id=place_id)


def _main():
    args = ArgumentParser(description=__doc__)
    args.add_argument("location", help="The geographic location to search")
    args.add_argument("--version", action="version", version=__version__)
    args.add_argument("--debug", "-d", action="store_true", help="Print exception stacktraces")
    args.add_argument("--config", "-c", default="config.json", help="The path to the configuration file")
    args.add_argument("--radius", "-r", type=int, help="The radius of the search in meters", default=8046)
    args.add_argument("-n", type=int, default=1, help="TThe maximum number of results to return")
    args.add_argument("--keyword", "-k", default="Restaurant",
                      help="The keyword to search for (use quotes around multiple keywords")
    args = args.parse_args()

    try:
        with open(args.config) as config_file:
            config = json.loads(config_file.read())
        key = config["key"]
        gmaps = googlemaps.Client(key=key)
        places = get_places(gmaps, args.keyword, args.location, radius=args.radius)
        random_places = _get_random_items(places, args.n)
        for i in range(len(random_places)):
            random_places[i] = get_place_details(gmaps, random_places[i]["place_id"])["result"]
        for place in random_places:
            print(f'{place["name"]}\n'
                  f'{place["formatted_address"]}')
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
