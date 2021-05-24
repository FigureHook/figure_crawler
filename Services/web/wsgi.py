# -*- coding: utf-8 -*-
"""Create an application instance."""
from gevent import monkey
monkey.patch_all()

from .app import create_app  # noqa:E402
app = create_app()
