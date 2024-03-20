# Les Aventuriers Numériques (LAN) / Site principal

Le [site web principal](https://team-lan.com/) de la team Les Aventuriers Numériques (LAN).

[![Publication](https://github.com/Les-Aventuriers-Numeriques/site-principal/actions/workflows/publish.yml/badge.svg)](https://github.com/Les-Aventuriers-Numeriques/site-principal/actions/workflows/publish.yml)

## Prérequis

  - Python >= 3.12
  - Un navigateur web moderne

## Installation

Clonez ce dépôt, puis le `pip install -r requirements.txt` habituel.

## Configuration

Définissez les variables d'environnement suivantes ou créez un fichier `.env` les contenant :

| Nom              | Type | Requis ? | Défaut | Description                                |
|------------------|------|----------|--------|--------------------------------------------|
| `SSH_USER`       | str  | Non      |        | Nom d'utilisateur SSH pour le déploiement  |
| `SSH_HOST`       | str  | Non      |        | Hôte cible du déploiement                  |
| `SSH_PATH`       | str  | Non      |        | Chemin absolu du répertoire de déploiement |

### Apache

Configuration du `VirtualHost` :

```apacheconf
ErrorDocument 404 /404.html
```

## Utilisation

Utilisez `invoke --list` afin de lister les tâches [Invoke](https://www.pyinvoke.org/) disponibles.

> [!NOTE]
> `invoke publish` nécessite `rsync` (i.e un environnement Linux).