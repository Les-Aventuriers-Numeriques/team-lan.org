from invoke import task, Context
from config import CONFIG
from environs import Env
import helpers

env = Env()
env.read_env()

CONFIG.update({
    'base_url': env.str('BASE_URL', CONFIG['base_url']),
    'minify_xml': env.bool('MINIFY_XML', CONFIG['minify_xml']),
})


@task
def clean(c: Context) -> None:
    """Supprime et recrée le répertoire du site généré"""
    print('Suppression et recréation de "{output_dir}"...'.format(**CONFIG))

    helpers.clean(CONFIG['output_dir'])


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
        CONFIG['assets_bundles'],
        CONFIG['minify_xml']
    ).render(watch)


@task
def serve(c: Context) -> None:
    """Permet de servir le site rendu via un serveur HTTP"""
    print('Lancement du serveur HTTP http://localhost:{serve_port}/ pour le répertoire {output_dir}...'.format(**CONFIG))

    helpers.serve(CONFIG['output_dir'], CONFIG['serve_port'])


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
