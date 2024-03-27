from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from webassets import Environment as AssetsEnvironment
from htmlmin import minify as minify_xml
from invoke import task, Context
from staticjinja import Site
from http import HTTPStatus
from jinja2 import Template
from config import CONFIG
from environs import Env
import shutil
import os

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

    if os.path.isdir(CONFIG['output_dir']):
        shutil.rmtree(CONFIG['output_dir'])

    os.makedirs(CONFIG['output_dir'])


@task
def build(c: Context, watch: bool = False) -> None:
    """Génère le rendu du site"""
    def build_url(path: str, absolute: bool = False) -> str:
        """Construit une URL vers un fichier"""
        url = CONFIG['base_url'].rstrip('/') + '/' if absolute else '/'
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

    print('Copie des fichiers statiques vers "{output_dir}"...'.format(**CONFIG))

    for file in CONFIG['static_files_to_copy']:
        dir_name = os.path.dirname(file)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        shutil.copy2(os.path.join(CONFIG['static_dir'], file), CONFIG['output_dir'])

    for directory in CONFIG['static_directories_to_copy']:
        shutil.copytree(os.path.join(CONFIG['static_dir'], directory), os.path.join(CONFIG['output_dir'], directory), dirs_exist_ok=True)

    print('Génération du rendu vers "{output_dir}"...'.format(**CONFIG))

    site = Site.make_site(
        outpath=CONFIG['output_dir'],
        mergecontexts=True,
        env_globals={
            'url': build_url,
        },
        contexts=CONFIG['contexts'],
        rules=[
            (r'.*\.(html|xml)', minify_template_xml)
        ] if CONFIG['minify_xml'] else None,
        extensions=['webassets.ext.jinja2.AssetsExtension']
    )

    site.env.assets_environment = AssetsEnvironment(directory=CONFIG['output_dir'], url='/', cache='static/.webassets-cache')
    site.env.assets_environment.append_path(CONFIG['static_dir'])

    for name, args, kwargs in CONFIG['assets_bundles']:
        site.env.assets_environment.register(name, *args, **kwargs)

    site.render(watch)


@task
def serve(c: Context) -> None:
    """Démarre un serveur HTTP servant le répertoire du site généré"""
    print('Lancement du serveur HTTP http://localhost:{serve_port}/ pour le répertoire {output_dir}...'.format(**CONFIG))

    class SimpleButEnhancedHTTPRequestHandler(SimpleHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def __init__(self, *args, **kvargs):
            try:
                super().__init__(*args, **kvargs, directory=CONFIG['output_dir'])
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

    with ThreadingHTTPServer(('127.0.0.1', CONFIG['serve_port']), SimpleButEnhancedHTTPRequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


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
