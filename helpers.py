from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from webassets import Environment as AssetsEnvironment
from typing import List, Tuple, Any, Dict
from staticjinja import Site
from http import HTTPStatus
from jinja2 import Template
import htmlmin
import shutil
import os


def clean(output_dir: str) -> None:
    """Supprime et recrée le répertoire du site généré"""
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir, exist_ok=True)


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
    """Copie les fichiers statiques (images, etc) dans le répertoire du site généré"""
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
        minify_xml: bool = False
) -> Site:
    """Crée une nouvelle instance `staticjinja.Site`"""
    def build_url(path: str, absolute: bool = False) -> str:
        """Construit une URL vers un fichier"""
        url = base_url.rstrip('/') + '/' if absolute else '/'
        url += path.lstrip('/')

        return url

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


def serve(output_dir: str, serve_port: int) -> None:
    """Démarre un serveur HTTP servant le répertoire du site généré"""
    class SimpleButEnhancedHTTPRequestHandler(SimpleHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def __init__(self, *args, **kvargs):
            try:
                super().__init__(*args, **kvargs, directory=output_dir)
            except ConnectionAbortedError:
                pass

        def translate_path(self, path):
            path = super().translate_path(path)

            # Emulation de la réécriture d'URLs d'un serveur web

            # Si on ne demande pas un répertoire
            if not path.endswith(('\\', '/')):
                _, extension = os.path.splitext(path)

                # Si pas d'extension de fichier dans le chemin
                if not extension:
                    # On considère qu'on veux afficher un fichier HTML
                    path += '.html'

            return path

        def send_error(self, code, message=None, explain=None):
            # Emulation de la page d'erreur 404 personnalisée définie au niveau du serveur web
            if self.command != 'HEAD' and code == HTTPStatus.NOT_FOUND: # Uniquement pour méthode HTTP != HEAD et erreur 404
                try:
                    f = open(os.path.join(self.directory, '404.html'), 'rb') # Si la page d'erreur personnalisée existe
                except OSError:
                    return super().send_error(code, message=message, explain=explain)

                fs = os.fstat(f.fileno())

                self.log_error("code %d, message %s", code, message)
                self.send_response(code, message)
                self.send_header('Connection', 'close')

                self.send_header('Content-Type', self.error_content_type)
                self.send_header('Content-Length', str(fs[6]))
                self.end_headers()

                self.copyfile(f, self.wfile)
            else:
                return super().send_error(code, message=message, explain=explain)

    with ThreadingHTTPServer(('127.0.0.1', serve_port), SimpleButEnhancedHTTPRequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
