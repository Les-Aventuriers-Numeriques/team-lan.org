<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://team-lan.org/images/logo_full_dark.png">
    <img src="https://team-lan.org/images/logo_full_light.png">
  </picture>
</p>

# Les Aventuriers Numériques / Site principal

Le [site institutionnel](https://team-lan.org/) de la team multigaming Les Aventuriers Numériques.

[![Publication](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml/badge.svg)](https://github.com/Les-Aventuriers-Numeriques/team-lan.org/actions/workflows/publish.yml)

Il s'agit d'un site statique simple généré à partir de templates [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) par
[staticjinjaplus](https://epocdotfr.github.io/staticjinjaplus/).

## Prérequis

  - Python >= 3.10 (développé sous 3.12)
  - Un navigateur web moderne

## Installation

Clonez ce dépôt, puis le `pip install -r requirements.txt` habituel.

## Configuration d'Apache

Configuration du `VirtualHost` :

```apacheconf
ErrorDocument 404 /404.html

RewriteEngine On

RewriteCond %{DOCUMENT_ROOT}%{REQUEST_FILENAME}.html -f
RewriteRule !.*\.html$ %{REQUEST_FILENAME}.html [L]
```
