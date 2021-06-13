#!/usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/scales.edthecoder.dev/")
sys.path.insert(0,"/var/www/scales.edthecoder.dev/scales")
sys.path.insert(0,"/var/www/scales.edthecoder.dev/scales/static")



from scales import app as application
application.secret_key = 'Add your secret key'