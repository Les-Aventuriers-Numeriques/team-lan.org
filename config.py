CONFIG = {
    'base_url': 'http://localhost:8080/',
    'append_html_to_urls': True,
    'minify_html': False,
    'output_dir': 'output',
    'static_dir': 'static',
    'site_name': 'Les Aventuriers Numériques',
    'site_description': 'Une team multigaming francophone et conviviale',
    'games_being_played': [
        578080, # PUBG
        526870, # Satisfactory
        504210, # SHENZHEN I/O
    ],
    'social_links': (
        ('discord', 'https://discord.team-lan.org/'),
        ('steam', 'https://steamcommunity.com/groups/Les-Aventuriers-Numeriques'),
        ('github', 'https://github.com/Les-Aventuriers-Numeriques'),
    ),
    'serve_port': 8080,
}