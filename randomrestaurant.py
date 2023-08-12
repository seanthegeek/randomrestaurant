#!/usr/bin/env python3

"""Returns random restaurants or other locations from Google Maps"""

import json
import sys
import traceback
from time import sleep
from random import shuffle
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import googlemaps
import googlemaps.geocoding
import googlemaps.places

__version__ = "1.1.0"


def _get_random_items(items: list, number: int = None) -> list:
    if number is not None:
        if number > len(items):
            number = len(items)
        _items = items.copy()
        shuffle(_items)
    return _items[:number]

def _bool_filter(items: list[dict], key: str) -> list:
    def _check_value(x: dict):
        if key not in x.keys():
            return False
        return x[key] is True
    filtered_items = items.copy()
    filtered_items = filter(_check_value, items)

    return list(filtered_items)


def get_places(gmaps: googlemaps.Client,
               keyword: str, near: str, radius=8046) -> list[dict]:
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
        response = googlemaps.places.places_nearby(
            gmaps,
            page_token=response["next_page_token"])
        results += response["results"]

    return results


def get_place_details(gmaps: googlemaps.Client, place_id: str) -> dict:
    return googlemaps.places.place(gmaps, place_id=place_id)["result"]


def _main():
    args = ArgumentParser(description=__doc__,
                          formatter_class=ArgumentDefaultsHelpFormatter)
    args.add_argument("location", help="The geographic location to search")
    args.add_argument("--version", action="version", version=__version__)
    args.add_argument("--debug", action="store_true",
                      help="Print exception stacktraces")
    args.add_argument("--config", "-c", default="config.json",
                      help="The path to the configuration file")
    args.add_argument("--radius", "-r", type=int,
                      help="The radius of the search area in meters",
                        default=8046)
    args.add_argument("-n", type=int, default=1,
                      help="The maximum number of results to return")
    args.add_argument("--keyword", "-k", default="Restaurant",
                      help="The keyword to search for "
                      "(Use quotes around multiple keywords)")
    args.add_argument("--delivery", "-d", action="store_true",
                      help="Only return locations that offer delivery")
    args.add_argument("--takeout", "-t", action="store_true",
                      help="Only return locations that offer takeout")
    args.add_argument("--wheelchair", "-w", action="store_true",
                      help="Only return locations that have a " 
                      "wheelchair-accessible entrance")
    args.add_argument("--json", "-j", action="store_true",
                      help="Output in JSON format")
    args = args.parse_args()

    try:
        with open(args.config) as config_file:
            config = json.loads(config_file.read())
        key = config["key"]
        gmaps = googlemaps.Client(key=key)
        places = get_places(gmaps, args.keyword, args.location,
                            radius=args.radius)
        for i in range(len(places)):
            places[i] = get_place_details(gmaps, places[i]["place_id"])
        if args.delivery:
            places = _bool_filter(places, "delivery")
        if args.takeout:
            places = _bool_filter(places, "takeout")
        if args.wheelchair:
            places = _bool_filter(places, "wheelchair_accessible_entrance")
        random_places = _get_random_items(places, args.n)
        if args.json:
            print(json.dumps(random_places, indent=2))
            exit()
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
