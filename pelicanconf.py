from datetime import date

# ----------------------------------------------------------
# Métadonnées

SITENAME = 'Les Aventuriers Numériques'
SITESUBTITLE = 'Une team multigaming francophone et conviviale'
AUTHOR = 'Le staff'

DEFAULT_METADATA = {
    'status': 'draft',
}

# ----------------------------------------------------------
# Développement

PORT = 8080

# ----------------------------------------------------------
# Chemins

PATH = 'content'

# ----------------------------------------------------------
# URLs

RELATIVE_URLS = True

SITEURL = 'http://localhost:8080'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = PAGE_URL + '.html'

ARCHIVES_SAVE_AS = INDEX_SAVE_AS = ''

ARTICLE_URL = ARTICLE_SAVE_AS = ''

CATEGORY_URL = CATEGORY_SAVE_AS = CATEGORIES_SAVE_AS = ''

TAG_URL = TAG_SAVE_AS = TAGS_SAVE_AS = ''

AUTHOR_URL = AUTHOR_SAVE_AS = AUTHORS_SAVE_AS = ''

DRAFT_URL = DRAFT_SAVE_AS = ''

DRAFT_PAGE_URL = DRAFT_PAGE_SAVE_AS = ''

# ----------------------------------------------------------
# URLs des flux

FEED_DOMAIN = SITEURL

RSS_FEED_SUMMARY_ONLY = False

FEED_ATOM = FEED_RSS = None
AUTHOR_FEED_ATOM = AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = TRANSLATION_FEED_RSS = None

FEED_ALL_ATOM = FEED_ALL_RSS = None

CATEGORY_FEED_ATOM = CATEGORY_FEED_RSS = None

TAG_FEED_ATOM = TAG_FEED_RSS = None

# ----------------------------------------------------------
# Internationalisation et localisation

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'
LOCALE = ('fr-FR', 'fr_FR', 'fr_FR.UTF8', 'fr_FR.UTF-8')

DATE_FORMATS = {
    'fr': '%-d %B %Y',
}

# ----------------------------------------------------------
# Catégories

DEFAULT_CATEGORY = 'Divers'

# ----------------------------------------------------------
# Plugins - tierce-partie

PLUGINS = [
    'seo',
    'sitemap',
    'htmlmin',
    'post_processings',
]

# pelican-seo

SEO_REPORT = False
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True
SEO_ENHANCER_SITEMAP_URL = SITEURL + '/sitemap.xml'
LOGO = SITEURL + '/images/logo_256.png' # TODO

# pelican-htmlmin

HTMLMIN_OPTIONS = {
    'remove_optional_attribute_quotes': False,
    'remove_empty_space': True,
    'remove_comments': True
}

# pelican-webassets

WEBASSETS_BUNDLES = (
     ('css_app', ('css/app.css', ), {'filters': 'cssutils', 'output': 'css/app.min.css'}),
)

# ----------------------------------------------------------
# Pagination

DEFAULT_PAGINATION = 10

PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/{number}', '{base_name}/{number}.html'),
)

# ----------------------------------------------------------
# Thème

THEME = './theme'

SOCIAL = (
    ('discord', 'https://discord.gg/vQYv4MfQf8'),
    ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
    ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
)
