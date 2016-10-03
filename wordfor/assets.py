# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'css/style.css',
    filters='cssmin',
    output='public/css/compiled/common.css'
)

js = Bundle(
    'libs/underscore/underscore.js',
    'libs/backbone/backbone.js',
    'libs/jQuery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    filters='rjsmin',
    output='public/js/compiled/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
