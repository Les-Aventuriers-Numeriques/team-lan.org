# Les Aventuriers Numériques / Site principal

Le [site web principal](https://team-lan.org/) de la team Les Aventuriers Numériques.

[![Publication](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml/badge.svg)](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml)

Il s'agit d'un site statique simple généré à partir de templates [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) par
[staticjinja](https://staticjinja.readthedocs.io/en/stable/index.html), avec quelques lignes de code permettant d'agrémenter
le tout.

## Prérequis

  - Python >= 3.12
  - Un navigateur web moderne

## Installation

Clonez ce dépôt, puis le `pip install -r requirements.txt` habituel.

## Configuration

### `config.py`

La configuration du site. Tous les chemins sont relatifs au répertoire racine, sauf mention contraire.

| Nom                          | Type                                            | Requis ? | Défaut                   | Description                                                                                                                                                                        |
|------------------------------|-------------------------------------------------|----------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SERVE_PORT`                 | int                                             | Non      | `8080`                   | Le port d'écoute du serveur HTTP lancé par `invoke serve`                                                                                                                          |
| `BASE_URL`                   | str                                             | Non      | `http://localhost:8080/` | Protocole et domaine de base pour les URLs absolues. La variable d'environnement associée est prioritaire lorsqu'elle est définie                                                  |
| `MINIFY_XML`                 | bool                                            | Non      | `False`                  | Minification ou non de l'XML (et par extension, de l'HTML également) résultant. La variable d'environnement associée est prioritaire lorsqu'elle est définie                       |
| `MINIFY_JSON`                | bool                                            | Non      | `False`                  | Minification ou non du JSON là où c'est nécessaire. La variable d'environnement associée est prioritaire lorsqu'elle est définie                                                   |
| `SEARCH_DIR`                 | str                                             | Non      | `templates`              | Le répertoire contenant les gabarits Jinja et le contenu                                                                                                                           |
| `OUTPUT_DIR`                 | str                                             | Non      | `output`                 | Le répertoire dans lequel le site rendu sera enregistré                                                                                                                            |
| `STATIC_DIR`                 | str                                             | Non      | `static`                 | Le répertoire contenant tous les fichiers statiques                                                                                                                                |
| `STATIC_FILES_TO_COPY`       | List[str]                                       | Non      | `[]`                     | La liste des fichiers statiques à copier (relatif à `STATIC_DIR`)                                                                                                                  |
| `STATIC_DIRECTORIES_TO_COPY` | List[str]                                       | Non      | `[]`                     | La liste des répertoires de fichiers statiques à copier (relatif à `STATIC_DIR`)                                                                                                   |
| `ASSETS_DIR`                 | str                                             | Non      | `assets`                 | Le répertoire contenant les fichiers qui nécessitent un traitement préalable afin d'être utilisés par le site rendu                                                                |
| `ASSETS_BUNDLES`             | List[Tuple[str, Tuple[str,...], Dict[str, str]] | Non      | `[]`                     | Les bundles [webassets](https://webassets.readthedocs.io/en/latest/) à utiliser dans les templates (les sources sont relatives à `ASSETS_DIR`, et les destinations à `OUTPUT_DIR`) |
| `CONTEXTS`                   | List[Tuple[str, Any]]                           | Non      | `[]`                     | Liste de [contextes staticjinja](https://staticjinja.readthedocs.io/en/stable/user/advanced.html#loading-data) à utiliser                                                          |

### Environnement

Les variables d'environnement suivantes sont destinées à être utilisées pour le déploiement du site (`invoke publish`).
Créez-les de façon classique ou dans un fichier `.env` les contenant.

| Nom           | Type | Requis ?                  | Défaut                      | Description                                                                    |
|---------------|------|---------------------------|-----------------------------|--------------------------------------------------------------------------------|
| `BASE_URL`    | str  | Non mais à définir        | Configuration `BASE_URL`    | Protocole et domaine de base pour les URLs absolues                            |
| `MINIFY_XML`  | bool | Non mais `True` conseillé | Configuration `MINIFY_XML`  | Minification ou non de l'XML (et par extension, de l'HTML également) résultant |
| `MINIFY_JSON` | bool | Non mais `True` conseillé | Configuration `MINIFY_JSON` | Minification ou non du JSON là où c'est nécessaire                             |
| `SSH_USER`    | str  | Oui                       |                             | Nom d'utilisateur pour le déploiement SSH                                      |
| `SSH_HOST`    | str  | Oui                       |                             | Hôte cible du déploiement SSH                                                  |
| `SSH_PORT`    | int  | Non                       | `22`                        | Port de l'hôte du déploiement SSH                                              |
| `SSH_PATH`    | str  | Oui                       |                             | Chemin absolu du répertoire de déploiement SSH                                 |

### Apache

Configuration du `VirtualHost` :

```apacheconf
ErrorDocument 404 /404.html

RewriteEngine On

RewriteCond %{DOCUMENT_ROOT}%{REQUEST_FILENAME}.html -f
RewriteRule !.*\.html$ %{REQUEST_FILENAME}.html [L]
```

## Utilisation

Utilisez `invoke --list` afin de lister les tâches [Invoke](https://www.pyinvoke.org/) disponibles.

> [!NOTE]
> `invoke publish` nécessite `rsync` (i.e un environnement Linux).