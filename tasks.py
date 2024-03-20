from staticjinja import Site
from environs import Env
from invoke import task
import shutil
import os

env = Env()
env.read_env()

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
def publish(c):
    """Publie le site en production (via rsync)"""
    CONFIG.update({
        'ssh_user': env.str('SSH_USER'),
        'ssh_host': env.str('SSH_HOST'),
        'ssh_port': 22,
        'ssh_path': env.str('SSH_PATH'),
    })

    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        '{} {ssh_user}@{ssh_host}:{ssh_path}'.format(
            CONFIG['outpath'].rstrip('/') + '/', **CONFIG
        )
    )
