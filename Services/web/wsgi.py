# -*- coding: utf-8 -*-
"""Create an application instance."""
from gevent import monkey
from .app import create_app

monkey.patch_all()
app = create_app()
