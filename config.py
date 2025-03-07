from babel.dates import get_timezone, format_date
from datetime import date, datetime

locale = 'fr_FR'
tzinfo = get_timezone('Europe/Paris')

USE_HTML_EXTENSION = False

WEBASSETS_BUNDLES = [
    ('css_base', ('css/base.css',), {'filters': 'rcssmin', 'output': 'css/base.min.css'}),
    ('css_lan', ('css/base.css', 'css/lan.css'), {'filters': 'rcssmin', 'output': 'css/lan.min.css'}),
]

team_name = 'Les Aventuriers Numériques'
motto = 'Une team multigaming francophone et conviviale'

CONTEXTS = [
    (r'index\.html', {
        'games_being_played': [
            (400750, 'Call to Arms - Gates of Hell'),
            (1239080, 'Door Kickers 2'),
            (2507950, 'Delta Force'),
            (394360, 'Hearts of Iron IV'),
            (686810, 'Hell Let Loose'),
            (232090, 'Killing Floor 2'),
            (1127400, 'Mindustry'),
            (578080, 'PUBG'),
            (270150, 'RUNNING WITH RIFLES'),
            (526870, 'Satisfactory'),
            (393380, 'Squad'),
            (236390, 'War Thunder'),
            (699130, 'World War Z'),
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
            (248610, 'Door Kickers'),
            (1250, 'Killing Floor'),
            ('https://losangelesmod.com/', 'lamod', 'Los Angeles Mod'),
             ('https://www.minecraft.net/fr-fr', 'mc', 'Minecraft'),
           (244450, 'Men of War: Assault Squad 2'),
            (453090, 'Parkitect'),
            (233450, 'Prison Architect'),
            ('https://www.realitymod.com/', 'pr', 'Project Reality: Battlefield 2'),
            (252950, 'Rocket League'),
            (377300, 'Thunder Tier One'),
        ],
    }),
    (r'lan\.html', {
        'current_attendees': 6,
        'max_attendees': 14,
        'start_date': date(2025, 11, 7),
        'end_date': date(2025, 11, 12),
        'location': {'name': 'Courtenay', 'url': 'https://maps.app.goo.gl/1pBpnWsVrg65qyNn9'},
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
