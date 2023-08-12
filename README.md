# randomrestaurant

```text
usage: randomrestaurant.py [-h] [--version] [--debug] [--config CONFIG] [--radius RADIUS] [-n N]
                           [--keyword KEYWORD] [--delivery] [--takeout] [--wheelchair] [--json]
                           location

Returns random restaurants or other locations from Google Maps

positional arguments:
  location              The geographic location to search

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               Print exception stacktraces
  --config CONFIG, -c CONFIG
                        The path to the configuration file
  --radius RADIUS, -r RADIUS
                        The radius of the search area in meters
  -n N                  The maximum number of results to return
  --keyword KEYWORD, -k KEYWORD
                        The keyword to search for (Use quotes around multiple keywords)
  --delivery, -d        Only return locations that offer delivery
  --takeout, -t         Only return locations that offer takeout
  --wheelchair, -w      Only return locations that have a wheelchair-accessible entrance
  --json, -j            Output in JSON format
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

Edit `config.json` and set the `key` value to the generated API key.

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
