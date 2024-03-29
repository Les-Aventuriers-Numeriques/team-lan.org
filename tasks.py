from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from webassets import Environment as AssetsEnvironment
from htmlmin import minify as minify_xml
from invoke import task, Context
from staticjinja import Site
from http import HTTPStatus
from jinja2 import Template
from copy import deepcopy
from environs import Env
import config as actual_config
import shutil
import os

default_config = {
    'SERVE_PORT': 8080,
    'BASE_URL': 'http://localhost:8080/',
    'MINIFY_XML': False,
    'OUTPUT_DIR': 'output',
    'STATIC_DIR': 'static',
    'STATIC_FILES_TO_COPY': [],
    'STATIC_DIRECTORIES_TO_COPY': [],
    'ASSETS_BUNDLES': [],
    'CONTEXTS': [],
}

config = deepcopy(default_config)
config.update({
    k: v for k, v in vars(actual_config).items() if k.isupper()
})


@task
def clean(c: Context) -> None:
    """Supprime et recrée le répertoire du site généré"""
    print('Suppression et recréation de "{OUTPUT_DIR}"...'.format(**config))

    if os.path.isdir(config['OUTPUT_DIR']):
        shutil.rmtree(config['OUTPUT_DIR'])

    os.makedirs(config['OUTPUT_DIR'])


@task
def build(c: Context, watch: bool = False) -> None:
    """Génère le rendu du site"""
    def build_url(path: str, absolute: bool = False) -> str:
        """Construit une URL vers un fichier"""
        url = config['BASE_URL'].rstrip('/') + '/' if absolute else '/'
        url += path.lstrip('/')

        return url

    def minify_template_xml(site: Site, template: Template, **kwargs) -> None:
        """Minifie le rendu d'un template Jinja XML (et par extension, HTML également)"""
        out = os.path.join(site.outpath, template.name)

        os.makedirs(os.path.dirname(out), exist_ok=True)

        with open(out, 'w', encoding=site.encoding) as f:
            f.write(
                minify_xml(
                    site.get_template(template.name).render(**kwargs),
                    remove_optional_attribute_quotes=False,
                    remove_empty_space=True,
                    remove_comments=True
                )
            )

    print('Copie des fichiers statiques vers "{OUTPUT_DIR}"...'.format(**config))

    for file in config['STATIC_FILES_TO_COPY']:
        dir_name = os.path.dirname(file)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        shutil.copy2(os.path.join(config['STATIC_DIR'], file), config['OUTPUT_DIR'])

    for directory in config['STATIC_DIRECTORIES_TO_COPY']:
        shutil.copytree(os.path.join(config['STATIC_DIR'], directory), os.path.join(config['OUTPUT_DIR'], directory), dirs_exist_ok=True)

    print('Génération du rendu vers "{OUTPUT_DIR}"...'.format(**config))

    site = Site.make_site(
        outpath=config['OUTPUT_DIR'],
        mergecontexts=True,
        env_globals={
            'url': build_url,
        },
        contexts=config['CONTEXTS'],
        rules=[
            (r'.*\.(html|xml)', minify_template_xml)
        ] if config['MINIFY_XML'] else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    site.env.assets_environment = AssetsEnvironment(directory=config['OUTPUT_DIR'], url='/', cache='static/.webassets-cache')
    site.env.assets_environment.append_path(config['STATIC_DIR'])

    for name, args, kwargs in config['ASSETS_BUNDLES']:
        site.env.assets_environment.register(name, *args, **kwargs)

    site.render(watch)


@task
def serve(c: Context) -> None:
    """Démarre un serveur HTTP servant le répertoire du site généré"""
    print('Lancement du serveur HTTP http://localhost:{SERVE_PORT}/ pour le répertoire {OUTPUT_DIR}...'.format(**config))

    class SimpleButEnhancedHTTPRequestHandler(SimpleHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def __init__(self, *args, **kvargs):
            try:
                super().__init__(*args, **kvargs, directory=config['OUTPUT_DIR'])
            except (ConnectionAbortedError, BrokenPipeError):
                pass

        def translate_path(self, path):
            path = super().translate_path(path)

            # Emulation de la réécriture d'URLs d'un serveur web

            # Si on ne demande pas un répertoire
            if not path.endswith(('\\', '/')):
                _, extension = os.path.splitext(path)

                # Si pas d'extension de fichier dans le chemin
                if not extension:
                    # On considère qu'on veut afficher un fichier HTML
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

    with ThreadingHTTPServer(('127.0.0.1', config['SERVE_PORT']), SimpleButEnhancedHTTPRequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


@task
def publish(c: Context) -> None:
    """Publie le site en production (avec `rsync`)"""
    env = Env()
    env.read_env()

    config.update({
        'BASE_URL': env.str('BASE_URL', config['BASE_URL']),
        'MINIFY_XML': env.bool('MINIFY_XML', config['MINIFY_XML']),
        'SSH_USER': env.str('SSH_USER'),
        'SSH_HOST': env.str('SSH_HOST'),
        'SSH_PORT': env.int('SSH_PORT', 22),
        'SSH_PATH': env.str('SSH_PATH'),
    })

    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {SSH_PORT}" '
        '{} {SSH_USER}@{SSH_HOST}:{SSH_PATH}'.format(
            config['OUTPUT_DIR'].rstrip('/') + '/', **config
        )
    )
