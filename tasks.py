from webassets import Environment as AssetsEnvironment
from staticjinja import Site
from config import CONFIG
from environs import Env
from invoke import task
import shutil
import os

env = Env()
env.read_env()


@task
def clean(c):
    """Supprime les fichiers générés"""
    print('Suppression et recréation de "{outpath}"...'.format(**CONFIG))

    if os.path.isdir(CONFIG['outpath']):
        shutil.rmtree(CONFIG['outpath'])
        os.makedirs(CONFIG['outpath'])


@task
def build(c, watch: bool = False):
    """Génère le rendu du site"""
    print('Copie des fichiers statiques vers "{outpath}"...'.format(**CONFIG))

    shutil.copy2('static/favicon.ico', os.path.join(CONFIG['outpath'], 'favicon.ico'))
    shutil.copytree('static/images', os.path.join(CONFIG['outpath'], 'static/images'))

    print('Génération du rendu dans vers "{outpath}"...'.format(**CONFIG))

    site = Site.make_site(
        outpath=CONFIG['outpath'],
        contexts=[
            ('index.html', {
                'games_being_played': CONFIG['games_being_played'],
                'social_links': CONFIG['social_links'],
            })
        ],
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    assets_environment = AssetsEnvironment(directory=os.path.join(CONFIG['outpath'], CONFIG['static_dir']), url=CONFIG['static_url_prefix'])
    assets_environment.append_path(CONFIG['static_dir'])

    site.env.assets_environment = assets_environment

    site.render(watch)


@task
def serve(c):
    """Permet de servir le site via HTTP"""
    c.run('python -m http.server -d {outpath} {serve_port}'.format(**CONFIG))


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
