# randomrestaurant

```text
usage: randomrestaurant.py [-h] [--version] [--debug] [--config CONFIG] [--radius RADIUS] [-n N] [--keyword KEYWORD]
                           [--delivery] [--takeout] [--wheelchair] [--json]
                           location

Returns random restaurants or other locations from Google Maps

positional arguments:
  location              the geographic location to search

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               print exception stacktraces (default: False)
  --config CONFIG, -c CONFIG
                        the path to the configuration file (default: config.json)
  --radius RADIUS, -r RADIUS
                        the radius of the search area in meters (default: 8046)
  -n N                  the maximum number of results to return (default: 1)
  --keyword KEYWORD, -k KEYWORD
                        the keyword to search for (use quotes around multiple keywords) (default: Restaurant)
  --delivery, -d        only return locations that offer delivery (default: False)
  --takeout, -t         only return locations that offer takeout (default: False)
  --wheelchair, -w      only return locations that have a wheelchair-accessible entrance (default: False)
  --json, -j            output in JSON format (default: False)
```

## Setup

Install `git` on your system using the Windows [installer][git-windows], your
package manager in Linux, or [`brew`][homebrew] on macOS. Then clone this
repository to your local system.

```bash
git clone https://github.com/seanthegeek/randomrestaurant.git
```

Generate a [Google Maps Platform][GMP] API key. Make sure that the key has
access to the following APIs:

- Geocoding API
- Geolocation API
- Places API

Create a file named `config.json` and set the `key` value to the generated API
key.

```json
{
    "key": ""
}
```

## Use

1. Open a terminal
2. `cd` to the directory where this repository was cloned
3. Use `./randomrestaurant.sh`in Linux or macOS, `randomrestaurant.bat` on the
   Windows command line, or `randomrestaurant.ps1` in Powershell on Windows

This wrapper script will automatically create a new
context of the new virtual environment and pas all arguments to it.
Python [virtual environment][venv] if needed, install any needed
dependencies. It will also execute `randomrestaurant.py` for you in the
context of the new virtual environment and pas all arguments to it.

[git-windows]: https://git-scm.com/download/win
[homebrew]: https://brew.sh/
[GMP]: https://developers.google.com/maps/get-started/
[venv]:  https://docs.python.org/3/library/venv.html
