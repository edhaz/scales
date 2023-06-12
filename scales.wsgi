import logging
import os
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/scales.edthecoder.dev/")
sys.path.insert(0, "/var/www/scales.edthecoder.dev/scales")
sys.path.insert(0, "/var/www/scales.edthecoder.dev/scales/static")


from scales import app as application

application.secret_key = environ.get("APP_SECRET_KEY", "not set")
