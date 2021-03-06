import copy
import os
from datetime import datetime
from itertools import groupby
from typing import Any

from pelican.utils import DateFormatter

from plugins import localdata

AUTHOR = "Maxime Le Conte des Floris"
SITENAME = "Films"
SITEURL = "https://films.mlcdf.fr"

PATH = "content"

TIMEZONE = "Europe/Rome"

DEFAULT_LANG = "fr"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "theme"
THEME_STATIC_DIR = "theme"

PAGE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}"

INDEX_SAVE_AS = "index.html"

STATIC_PATHS = ["extra", "images"]

EXTRA_PATH_METADATA = {
    "extra/humans.txt": {"path": "humans.txt"},
}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {
            "permalink": "#",
            "permalink_title": "Lien permanent",
            "baselevel": 2,
        },
    },
    "extensions": [],
    "output_format": "html5",
}

JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.loopcontrols"]}
JINJA_GLOBALS = {
    "now": datetime.now,
    "strftime": DateFormatter,
}

PLUGINS_PATH = ["./plugins"]
PLUGINS = [localdata]


def aria_hidden(txt: str) -> str:
    return (
        txt.replace("🗒", "<span aria-hidden='true'>🗒</span>")
        .replace("📽️", "<span aria-hidden='true'>📽️</span>")
        .replace("💗", "<span aria-hidden='true'>💗</span>")
    )


def groupby_year(value):
    def key(v):
        return v["done_date"].year

    return groupby(sorted(value, key=key, reverse=True), key)


JINJA_FILTERS = {
    "aria_hidden": aria_hidden,
    "groupby_year": groupby_year
}

TEMPLATE_PAGES = {
    os.path.join(os.getcwd(), "theme/templates/love.html"): "love/index.html",
    os.path.join(os.getcwd(), "theme/templates/wish.html"): "wish/index.html",
}

DATA_PATH = "data"
