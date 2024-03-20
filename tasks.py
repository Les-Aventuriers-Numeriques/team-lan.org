from staticjinja import Site
from invoke import task
import shutil
import os

CONFIG = {
    'outpath': 'output',
    'games_being_played': [
        578080, # PUBG
        526870, # Satisfactory
        504210, # SHENZHEN I/O
    ]
}


@task
def clean(c):
    """Supprime les fichiers générés"""
    print('Suppression et recréation du dossier "{}"...'.format(CONFIG['outpath']))

    if os.path.isdir(CONFIG['outpath']):
        shutil.rmtree(CONFIG['outpath'])
        os.makedirs(CONFIG['outpath'])


@task
def build(c):
    """Génère le rendu statique du site"""
    print('Génération du rendu dans le dossier "{}"...'.format(CONFIG['outpath']))

    site = Site.make_site(
        outpath=CONFIG['outpath'],
        contexts=[
            ('index.html', {
                'games_being_played': CONFIG['games_being_played']
            })
        ]
    )

    site.render()


@task
def deploy(c):
    """Déploie en production (via rsync)"""
    pass
