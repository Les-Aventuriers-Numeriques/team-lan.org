STATIC_FILES_TO_COPY = [
    'favicon.ico',
]

STATIC_DIRECTORIES_TO_COPY = [
    'images',
]

ASSETS_BUNDLES = [
    ('css_base', ('css/base.css',), {'filters': 'cssutils', 'output': 'css/base.min.css'}),
    ('css_lan', ('css/base.css', 'css/lan.css'), {'filters': 'cssutils', 'output': 'css/lan.min.css'}),
]
