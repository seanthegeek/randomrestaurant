echo off

if not exists .venv\ {
    python3 -m venv .venv
    .venv\Scripts\pip.exe install -U pip
    .venv\Scripts\pip.exe install -U -r requirements.txt
}

.venv\Scripts\python.exe randomrestaurant.py %*
