from webassets import Environment as AssetsEnvironment
from invoke import task, Context
from markupsafe import Markup
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


def _read_svg_icon(name: str) -> Markup:
    with open(os.path.join('static', 'images', f'{name}.svg'), 'r') as f:
        return Markup(f'<span class="social-icon {name}">{f.read()}</span>')


@task
def clean(c: Context) -> None:
    """Supprime les fichiers générés"""
    print('Suppression et recréation de "{output_dir}"...'.format(**CONFIG))

    if os.path.isdir(CONFIG['output_dir']):
        shutil.rmtree(CONFIG['output_dir'])
        os.makedirs(CONFIG['output_dir'])


@task
def build(c: Context, watch: bool = False, compress: bool = False) -> None:
    """Génère le rendu du site"""
    print('Copie des fichiers statiques vers "{output_dir}"...'.format(**CONFIG))

    shutil.copy2('static/favicon.ico', os.path.join(CONFIG['output_dir'], 'favicon.ico'))
    shutil.copytree('static/images', os.path.join(CONFIG['output_dir'], 'static', 'images'))

    print('Génération du rendu dans vers "{output_dir}"...'.format(**CONFIG))

    site = Site.make_site(
        outpath=CONFIG['output_dir'],
        mergecontexts=True,
        env_globals={
            'icon': _read_svg_icon,
        },
        contexts=[
            ('index.html', {
                'games_being_played': CONFIG['games_being_played'],
                'social_links': CONFIG['social_links'],
            }),
            (r'.*\.html', {
                'site_name': CONFIG['site_name'],
                'site_description': CONFIG['site_description'],
            })
        ],
        rules=[
            (r'.*\.html', _minify_html)
        ] if compress else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    assets_environment = AssetsEnvironment(directory=os.path.join(CONFIG['output_dir'], CONFIG['static_dir']), url=CONFIG['static_url_prefix'])
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
