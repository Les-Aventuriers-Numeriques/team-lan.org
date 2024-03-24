from datetime import datetime

CONFIG = {
    'serve_port': 8080,
    'base_url': 'http://localhost:8080/',
    'minify_xml': False,
    'output_dir': 'output',
    'static_dir': 'static',
    'remove_html_extension': False,
    'static_files_to_copy': [
        'favicon.ico',
    ],
    'static_directories_to_copy': [
        'images',
    ],
    'contexts': [
        (r'index\.html', {
            'games_being_played': [
                (578080, 'PUBG'),
                (526870, 'Satisfactory'),
                (504210, 'SHENZHEN I/O'),
            ],
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
