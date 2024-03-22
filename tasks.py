from webassets import Environment as AssetsEnvironment
from invoke import task, Context
from datetime import datetime
from staticjinja import Site
from jinja2 import Template
from config import CONFIG
from environs import Env
from pathlib import Path
import htmlmin
import shutil
import os

env = Env()
env.read_env()

CONFIG.update({
    'base_url': env.str('BASE_URL', CONFIG['base_url']),
    'append_html_to_urls': env.bool('APPEND_HTML_TO_URLS', CONFIG['append_html_to_urls']),
    'compress_html': env.bool('COMPRESS_HTML', CONFIG['compress_html']),
})


def _minify_html(site: Site, template: Template, **kwargs) -> None:
    out = site.outpath / Path(template.name).with_suffix('.html')

    os.makedirs(out.parent, exist_ok=True)

    with open(str(out), 'w', encoding=site.encoding) as f:
        f.write(
            htmlmin.minify(
                site.get_template(template.name).render(**kwargs),
                remove_optional_attribute_quotes=False,
                remove_empty_space=True,
                remove_comments=True
            )
        )


def _build_static_url(path: str, absolute: bool = False) -> str:
    url = CONFIG['base_url'].rstrip('/') + '/' if absolute else '/'
    url += path.lstrip('/')

    return url


def _build_url(path: str, absolute: bool = False) -> str:
    url = _build_static_url(path, absolute)

    if CONFIG['append_html_to_urls']:
        url += '.html'

    return url


@task
def clean(c: Context) -> None:
    """Supprime les fichiers générés"""
    print('Suppression et recréation de "{output_dir}"...'.format(**CONFIG))

    if os.path.isdir(CONFIG['output_dir']):
        shutil.rmtree(CONFIG['output_dir'])
        os.makedirs(CONFIG['output_dir'])


@task
def build(c: Context, watch: bool = False) -> None:
    """Génère le rendu du site"""
    print('Copie des fichiers statiques vers "{output_dir}"...'.format(**CONFIG))

    shutil.copy2('static/favicon.ico', os.path.join(CONFIG['output_dir'], 'favicon.ico'))
    shutil.copytree('static/images', os.path.join(CONFIG['output_dir'], 'images'))

    print('Génération du rendu vers "{output_dir}"...'.format(**CONFIG))

    site = Site.make_site(
        outpath=CONFIG['output_dir'],
        mergecontexts=True,
        env_globals={
            'url': _build_url,
            'static_url': _build_static_url,
        },
        contexts=[
            ('index.html', {
                'games_being_played': CONFIG['games_being_played'],
            }),
            (r'.*\.html', {
                'social_links': CONFIG['social_links'],
                'site_name': CONFIG['site_name'],
                'site_description': CONFIG['site_description'],
                'current_year': datetime.now().year,
            })
        ],
        rules=[
            (r'.*\.html', _minify_html)
        ] if CONFIG['compress_html'] else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    assets_environment = AssetsEnvironment(directory=CONFIG['output_dir'], url='/')
    assets_environment.append_path(CONFIG['static_dir'])

    site.env.assets_environment = assets_environment

    site.render(watch)


@task
def serve(c: Context) -> None:
    """Permet de servir le site via HTTP"""
    c.run('python -m http.server -d {output_dir} {serve_port}'.format(**CONFIG))


@task
def publish(c: Context) -> None:
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
            CONFIG['output_dir'].rstrip('/') + '/', **CONFIG
        )
    )
