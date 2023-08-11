set -e

if [ ! -d ".venv" ]; then
    # Use system CAs with pip
    if [ -d /etc/ssl/certs/ ]; then
      # Debian/Ubuntu
      export PIP_CERT=/etc/ssl/certs/
      elif [ -d /etc/pki/ca-trust/extracted ]; then
        # Arch/CentOS/RHEL/Rocky
        export PIP_CERT=/etc/pki/ca-trust/extracted
      elif [ -f /etc/ssl/cert.pem ]; then
        # macOS
        export PIP_CERT=/etc/ssl/cert.pem
    fi
    virtualenv .venv || exit
    . .venv/bin/activate
    pip install -U pip
    pip install -U -r requirements.txt
fi

.venv/bin/python3 randomrestaurant.py "$@"
