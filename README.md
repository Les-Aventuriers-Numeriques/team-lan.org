# Les Aventuriers Numériques / Site principal

Le [site web principal](https://team-lan.org/) de la team Les Aventuriers Numériques.

[![Publication](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml/badge.svg)](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml)

## Prérequis

  - Python >= 3.12
  - Un navigateur web moderne

## Installation

Clonez ce dépôt, puis le `pip install -r requirements.txt` habituel.

## Configuration

Définissez les variables d'environnement suivantes ou créez un fichier `.env` les contenant :

| Nom          | Type | Requis ?               | Défaut                   | Description                                                                              |
|--------------|------|------------------------|--------------------------|------------------------------------------------------------------------------------------|
| `BASE_URL`   | str  | Non                    | `http://localhost:8080/` | Protocole et domaine de base pour les URLs absolues                                      |
| `MINIFY_XML` | bool | Non                    | `False`                  | Minification ou non de l'XML (et par extension, de l'HTML également) résultant  du rendu |
| `SSH_USER`   | str  | Déploiement uniquement |                          | Nom d'utilisateur SSH pour le déploiement                                                |
| `SSH_HOST`   | str  | Déploiement uniquement |                          | Hôte cible du déploiement                                                                |
| `SSH_PORT`   | int  | Déploiement uniquement | `22`                     | Port de l'hôte du déploiement                                                            |
| `SSH_PATH`   | str  | Déploiement uniquement |                          | Chemin absolu du répertoire de déploiement                                               |

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