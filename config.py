from datetime import datetime

CONFIG = {
    'serve_port': 8080,
    'base_url': 'http://localhost:8080/',
    'minify_xml': False,
    'output_dir': 'output',
    'static_dir': 'static',
    'static_files_to_copy': [
        'favicon.ico',
    ],
    'static_directories_to_copy': [
        'images',
    ],
    'assets_bundles': [
        ('css_base', ('css/base.css',), {'filters': 'cssutils', 'output': 'css/base.min.css'}),
        ('css_index', ('css/base.css', 'css/index.css'), {'filters': 'cssutils', 'output': 'css/index.min.css'}),
    ],
    'contexts': [
        (r'index\.html', {
            'games_being_played': [
                (1158310, 'Crusader Kings III'),
                (394360, 'Hearts of Iron IV'),
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
                (248610, 'Door Kickers'),
                (1250, 'Killing Floor'),
                ('https://losangelesmod.com/', 'lamod', 'Los Angeles Mod'),
                (244450, 'Men of War: Assault Squad 2'),
                (453090, 'Parkitect'),
                (233450, 'Prison Architect'),
                ('https://www.realitymod.com/', 'pr', 'Project Reality: Battlefield 2'),
                (252950, 'Rocket League'),
                (270150, 'RUNNING WITH RIFLES'),
                (393380, 'Squad'),
                (377300, 'Thunder Tier One'),
            ]
        }),
        (r'.*\.html', {
            'social_links': [
                ('discord', 'https://discord.team-lan.org/'),
                ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
                ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
            ],
            'site_name': 'Les Aventuriers Numériques',
            'site_description': 'Une team multigaming francophone et conviviale',
            'current_year': datetime.now().year,
        })
    ]
}
