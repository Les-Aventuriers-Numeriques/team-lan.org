from datetime import date

LOCALE = ['fr-FR', 'fr_FR', 'fr_FR.UTF8', 'fr_FR.UTF-8']

ASSETS_BUNDLES = [
    ('css_base', ('css/base.css',), {'filters': 'cssutils', 'output': 'css/base.min.css'}),
    ('css_lan', ('css/base.css', 'css/lan.css'), {'filters': 'cssutils', 'output': 'css/lan.min.css'}),
]

lan_current_attendees = 8
lan_max_attendees = 10
team_name = 'Les Aventuriers Numériques'
motto = 'Une team multigaming francophone et conviviale'

CONTEXTS = [
    (r'index\.html', {
        'games_being_played': [
            (1158310, 'Crusader Kings III'),
            (1239080, 'Door Kickers 2'),
            (394360, 'Hearts of Iron IV'),
            (686810, 'Hell Let Loose'),
            (232090, 'Killing Floor 2'),
            (578080, 'PUBG'),
            (526870, 'Satisfactory'),
        ],
        'previously_played_games': [
            (1015140, '10 Miles To Safety'),
            (33900, 'Arma 2'),
            (107410, 'Arma 3'),
            (813780, 'Age of Empires II'),
            (681590, 'Blitzkrieg Mod'),
            (302670, 'Call to Arms'),
            (231430, 'Company of Heroes 2'),
            (248610, 'Door Kickers'),
            (1250, 'Killing Floor'),
            ('https://losangelesmod.com/', 'lamod', 'Los Angeles Mod'),
            (244450, 'Men of War: Assault Squad 2'),
            (1127400, 'Mindustry'),
            (453090, 'Parkitect'),
            (233450, 'Prison Architect'),
            ('https://www.realitymod.com/', 'pr', 'Project Reality: Battlefield 2'),
            (252950, 'Rocket League'),
            (270150, 'RUNNING WITH RIFLES'),
            (393380, 'Squad'),
            (377300, 'Thunder Tier One'),
            (236390, 'War Thunder'),
        ],
    }),
    (r'lan\.html', {
        'current_attendees': lan_current_attendees,
        'max_attendees': lan_max_attendees,
        'start_date': date(2024, 11, 7),
        'end_date': date(2024, 11, 11),
        'location': {
            'name': 'Rully',
            'url': 'https://maps.app.goo.gl/5Azz9MJbAin44MUt6',
        },
        'lan_games': [],
    }),
]

GLOBALS = {
    'social_links': [
        ('discord', 'https://discord.gg/vQYv4MfQf8'),
        ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
        ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
    ],
    'team_name': team_name,
    'motto': motto,
    'today': date.today(),
    'team_founded': date(2024, 3, 8),
}
