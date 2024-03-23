from datetime import datetime

games_being_played = [
    (578080, 'PUBG'),
    (526870, 'Satisfactory'),
    (504210, 'SHENZHEN I/O'),
]

social_links = [
    ('discord', 'https://discord.team-lan.org/'),
    ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
    ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
]

site_name = 'Les Aventuriers Numériques'
site_description = 'Une team multigaming francophone et conviviale'

CONFIG = {
    'serve_port': 8080,
    'base_url': 'http://localhost:8080/',
    'append_html_to_urls': True,
    'minify_html': False,
    'output_dir': 'output',
    'static_dir': 'static',
    'static_files_to_copy': [
        'favicon.ico',
    ],
    'static_directories_to_copy': [
        'images',
    ],
    'contexts': [
        ('index.html', {
            'games_being_played': games_being_played,
        }),
        (r'.*\.html', {
            'social_links': social_links,
            'site_name': site_name,
            'site_description': site_description,
            'current_year': datetime.now().year,
        })
    ]
}
