from babel.dates import get_timezone, format_date
from datetime import date, datetime

locale = 'fr_FR'
tzinfo = get_timezone('Europe/Paris')

USE_HTML_EXTENSION = False

WEBASSETS_BUNDLES = [
    ('css_base', ('css/base.css',), {'filters': 'rcssmin', 'output': 'css/base.css'}),
    ('css_lan', ('css/base.css', 'css/lan.css'), {'filters': 'rcssmin', 'output': 'css/lan.css'}),
]

team_name = 'Les Aventuriers Numériques'
motto = 'Une team multigaming francophone et conviviale'

CONTEXTS = [
    (r'index\.html', {
        'games_being_played': [
            (1604270, 'Broken Arrow'),
            (400750, 'Call to Arms - Gates of Hell'),
            (1239080, 'Door Kickers 2'),
            (394360, 'Hearts of Iron IV'),
            (1127400, 'Mindustry'),
            (453090, 'Parkitect'),
            (252490, 'Rust'),
            (526870, 'Satisfactory'),
            (393380, 'Squad'),
        ],
        'previously_played_games': [
            (1015140, '10 Miles To Safety'),
            (33900, 'Arma 2'),
            (107410, 'Arma 3'),
            (813780, 'Age of Empires II'),
            (681590, 'Blitzkrieg Mod'),
            (302670, 'Call to Arms'),
            (228200, 'Company of Heroes'),
            (231430, 'Company of Heroes 2'),
            (1158310, 'Crusader Kings III'),
            (2507950, 'Delta Force'),
            (248610, 'Door Kickers'),
            (686810, 'Hell Let Loose'),
            (1250, 'Killing Floor'),
            (232090, 'Killing Floor 2'),
            ('https://losangelesmod.com/', 'lamod', 'Los Angeles Mod'),
            ('https://www.minecraft.net/fr-fr', 'mc', 'Minecraft'),
            (244450, 'Men of War: Assault Squad 2'),
            (233450, 'Prison Architect'),
            (578080, 'PUBG'),
            ('https://www.realitymod.com/', 'pr', 'Project Reality: Battlefield 2'),
            (252950, 'Rocket League'),
            (270150, 'RUNNING WITH RIFLES'),
            (377300, 'Thunder Tier One'),
            (236390, 'War Thunder'),
            (699130, 'World War Z'),
        ],
    }),
    (r'lan\.html', {
        'current_attendees': None, # 8,
        'max_attendees': None, # 14,
        'start_date': None, # date(2025, 11, 7),
        'end_date': None, # date(2025, 11, 12),
        'location': None, # {'name': 'Courtenay', 'url': 'https://maps.app.goo.gl/1pBpnWsVrg65qyNn9'},
    }),
]

JINJA_GLOBALS = {
    'social_links': [
        ('discord', 'https://discord.gg/vQYv4MfQf8'),
        ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
        ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
    ],
    'team_name': team_name,
    'motto': motto,
    'now': datetime.now(tz=tzinfo),
    'team_founded': date(2024, 3, 8),
}


def dateformat(*args, **kwargs):
    return format_date(*args, **kwargs, locale=locale)


JINJA_FILTERS = {
    'dateformat': dateformat,
}
