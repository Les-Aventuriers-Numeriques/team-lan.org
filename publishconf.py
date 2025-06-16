# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# ----------------------------------------------------------
# URLs

SITEURL = 'https://team-lan.org'

RELATIVE_URLS = False

# ----------------------------------------------------------
# Plugins - tierce-partie

# pelican-seo

SEO_ENHANCER_SITEMAP_URL = SITEURL + '/sitemap.xml'
LOGO = SITEURL + '/images/logo_256.png' # TODO

# ----------------------------------------------------------
# Autres

DELETE_OUTPUT_DIRECTORY = True