#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Root __init__
"""

import logging
from logging import getLogger as get_logger

__author__ = "Samuel Marks"
__version__ = "0.0.5"
__description__ = (
    "Migration tooling from Google App Engine (webapp2, ndb)"
    " to python-cdd supported (FastAPI, SQLalchemy)."
)


root_logger = get_logger()
logging.getLogger("blib2to3").setLevel(logging.WARNING)

__all__ = ["get_logger", "root_logger", "__description__", "__version__"]
