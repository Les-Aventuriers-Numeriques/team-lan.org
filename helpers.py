from webassets import Environment as AssetsEnvironment
from staticjinja import Site
from jinja2 import Template
from config import CONFIG
from pathlib import Path
import htmlmin
import shutil
import os


def minify_html(site: Site, template: Template, **kwargs) -> None:
    """Minifie le HTML du rendu d'un template Jinja"""
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


def build_static_url(path: str, absolute: bool = False) -> str:
    """Construit une URL vers un fichier statique"""
    url = CONFIG['base_url'].rstrip('/') + '/' if absolute else '/'
    url += path.lstrip('/')

    return url


def build_url(path: str, absolute: bool = False) -> str:
    """Pareil que `_build_static_url()`, sauf que ça rajoute `.html` à la fin si configuré comme tel"""
    url = build_static_url(path, absolute)

    if path and CONFIG['append_html_to_urls']:
        url += '.html'

    return url


def copy_static_assets() -> None:
    for file in CONFIG['static_files_to_copy']:
        dir_name = os.path.dirname(file)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        shutil.copy2(os.path.join(CONFIG['static_dir'], file), CONFIG['output_dir'])

    for directory in CONFIG['static_directories_to_copy']:
        shutil.copytree(os.path.join(CONFIG['static_dir'], directory), os.path.join(CONFIG['output_dir'], directory), dirs_exist_ok=True)


def create_assets_environment() -> AssetsEnvironment:
    """Crée une nouvelle instance `AssetsEnvironment`"""
    assets_environment = AssetsEnvironment(directory=CONFIG['output_dir'], url='/', cache='static/.webassets-cache')
    assets_environment.append_path(CONFIG['static_dir'])

    return assets_environment


def create_site_builder() -> Site:
    """Crée une nouvelle instance `Site`"""
    site = Site.make_site(
        outpath=CONFIG['output_dir'],
        mergecontexts=True,
        env_globals={
            'url': build_url,
            'static_url': build_static_url,
        },
        contexts=CONFIG['contexts'],
        rules=[
            (r'.*\.html', minify_html)
        ] if CONFIG['minify_html'] else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    site.env.assets_environment = create_assets_environment()

    return site
