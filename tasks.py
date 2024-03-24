from invoke import task, Context
from config import CONFIG
from environs import Env
import helpers
import shutil
import os

env = Env()
env.read_env()

CONFIG.update({
    'base_url': env.str('BASE_URL', CONFIG['base_url']),
    'minify_xml': env.bool('MINIFY_XML', CONFIG['minify_xml']),
    'remove_html_extension': env.bool('REMOVE_HTML_EXTENSION', CONFIG['remove_html_extension']),
})


@task
def clean(c: Context) -> None:
    """Supprime les fichiers générés"""
    print('Suppression et recréation de "{output_dir}"...'.format(**CONFIG))

    if os.path.isdir(CONFIG['output_dir']):
        shutil.rmtree(CONFIG['output_dir'])

    os.makedirs(CONFIG['output_dir'], exist_ok=True)


@task
def build(c: Context, watch: bool = False) -> None:
    """Génère le rendu du site"""
    print('Copie des fichiers statiques vers "{output_dir}"...'.format(**CONFIG))

    helpers.copy_static_assets(
        CONFIG['output_dir'],
        CONFIG['static_dir'],
        CONFIG['static_files_to_copy'],
        CONFIG['static_directories_to_copy']
    )

    print('Génération du rendu vers "{output_dir}"...'.format(**CONFIG))

    helpers.create_site_builder(
        CONFIG['base_url'],
        CONFIG['output_dir'],
        CONFIG['static_dir'],
        CONFIG['contexts'],
        CONFIG['minify_xml'],
        CONFIG['remove_html_extension']
    ).render(watch)


@task
def serve(c: Context) -> None:
    """Permet de servir le site rendu via un serveur HTTP"""
    c.run('python -m http.server -d {output_dir} -p HTTP/1.1 {serve_port}'.format(**CONFIG))


@task
def publish(c: Context) -> None:
    """Publie le site en production (avec `rsync`)"""
    CONFIG.update({
        'ssh_user': env.str('SSH_USER'),
        'ssh_host': env.str('SSH_HOST'),
        'ssh_port': env.int('SSH_PORT', 22),
        'ssh_path': env.str('SSH_PATH'),
    })

    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        '{} {ssh_user}@{ssh_host}:{ssh_path}'.format(
            CONFIG['output_dir'].rstrip('/') + '/', **CONFIG
        )
    )
