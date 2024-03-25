from webassets import Environment as AssetsEnvironment
from typing import List, Tuple, Any, Dict
from staticjinja import Site
from jinja2 import Template
import htmlmin
import shutil
import os


def minify_template_xml(site: Site, template: Template, **kwargs) -> None:
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


def copy_static_assets(
        output_dir: str,
        static_dir: str,
        static_files_to_copy: List[str],
        static_directories_to_copy: List[str]
) -> None:
    for file in static_files_to_copy:
        dir_name = os.path.dirname(file)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        shutil.copy2(os.path.join(static_dir, file), output_dir)

    for directory in static_directories_to_copy:
        shutil.copytree(os.path.join(static_dir, directory), os.path.join(output_dir, directory), dirs_exist_ok=True)


def create_site_builder(
        base_url: str,
        output_dir: str,
        static_dir: str,
        contexts: List[Tuple[str, dict[str, Any]]],
        assets_bundles: List[Tuple[str, Tuple[str,...], Dict[str, str]]],
        minify_xml: bool = False,
        remove_html_extension: bool = False
) -> Site:
    """Crée une nouvelle instance `Site`"""
    def build_url(path: str, absolute: bool = False) -> str:
        """Construit une URL vers un fichier"""
        url = base_url.rstrip('/') + '/' if absolute else '/'
        url += path.lstrip('/')

        return url if not remove_html_extension else url.removesuffix('.html')

    site = Site.make_site(
        outpath=output_dir,
        mergecontexts=True,
        env_globals={
            'url': build_url,
        },
        contexts=contexts,
        rules=[
            (r'.*\.(html|xml)', minify_template_xml)
        ] if minify_xml else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    site.env.assets_environment = AssetsEnvironment(directory=output_dir, url='/', cache='static/.webassets-cache')
    site.env.assets_environment.append_path(static_dir)

    for name, args, kwargs in assets_bundles:
        site.env.assets_environment.register(name, *args, **kwargs)

    return site
