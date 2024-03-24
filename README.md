# Les Aventuriers Numériques / Site principal

Le [site web principal](https://team-lan.org/) de la team Les Aventuriers Numériques.

[![Publication](https://github.com/Les-Aventuriers-Numeriques/site-principal/actions/workflows/publish.yml/badge.svg)](https://github.com/Les-Aventuriers-Numeriques/site-principal/actions/workflows/publish.yml)

## Prérequis

  - Python >= 3.12
  - Un navigateur web moderne

## Installation

Clonez ce dépôt, puis le `pip install -r requirements.txt` habituel.

## Configuration

Définissez les variables d'environnement suivantes ou créez un fichier `.env` les contenant :

| Nom                     | Type | Requis ? | Défaut                            | Description                                                               |
|-------------------------|------|----------|-----------------------------------|---------------------------------------------------------------------------|
| `BASE_URL`              | str  | Non      | `CONFIG['base_url']`              | Protocole et domaine de base pour les URLs absolues                       |
| `MINIFY_XML`            | bool | Non      | `CONFIG['minify_xml']`            | Minification ou non de l'XML (et par extension, HTML également) résultant |
| `REMOVE_HTML_EXTENSION` | bool | Non      | `CONFIG['remove_html_extension']` | Supprime ou non l'extension' `.html` des URLs générées                    |
| `SSH_USER`              | str  | Non      |                                   | Nom d'utilisateur SSH pour le déploiement                                 |
| `SSH_HOST`              | str  | Non      |                                   | Hôte cible du déploiement                                                 |
| `SSH_PORT`              | int  | Non      | `22`                              | Port de l'hôte du déploiement                                             |
| `SSH_PATH`              | str  | Non      |                                   | Chemin absolu du répertoire de déploiement                                |

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