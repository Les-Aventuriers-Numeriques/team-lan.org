from webassets import Environment as AssetsEnvironment
from staticjinja import Site
from jinja2 import Template
from config import CONFIG
import htmlmin
import shutil
import os


def minify_xml(site: Site, template: Template, **kwargs) -> None:
    """Minifie le rendu d'un template Jinja XML (et par extension, HTML également)"""
    out = os.path.join(site.outpath, template.name)

    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(out, 'w', encoding=site.encoding) as f:
        f.write(
            htmlmin.minify(
                site.get_template(template.name).render(**kwargs),
                remove_optional_attribute_quotes=False,
                remove_empty_space=True,
                remove_comments=True
            )
        )


def build_url(path: str, absolute: bool = False) -> str:
    """Construit une URL vers un fichier"""
    url = CONFIG['base_url'].rstrip('/') + '/' if absolute else '/'
    url += path.lstrip('/')

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
        },
        contexts=CONFIG['contexts'],
        rules=[
            (r'.*\.(html|xml)', minify_xml)
        ] if CONFIG['minify_xml'] else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    site.env.assets_environment = create_assets_environment()

    return site
