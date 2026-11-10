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

  - Python >= 3.10 (développé sous 3.14)
  - Node.js et n'importe quel gestionnaire de paquets à la mode actuellement
  - [Pipenv](https://pipenv.pypa.io/en/latest/)
  - Un navigateur web moderne

## Installation

  1. Clonez ce dépôt
  2. `pipenv install --dev`
  3. `npm install`

## Configuration d'Apache

Configuration du `VirtualHost` :

```apacheconf
AddType application/rss+xml .rss
AddType application/atom+xml .atom

ErrorDocument 404 /404.html

RewriteEngine On

RewriteCond %{THE_REQUEST} ^[A-Z]+\s[^\s?]*/index(\.html)?[\s?]
RewriteRule ^(.*/)index(\.html)?$ $1 [R=301,L]

RewriteCond %{THE_REQUEST} ^[A-Z]+\s[^\s?]+\.html[\s?]
RewriteRule ^(.+)\.html$ $1 [R=301,L]

RewriteCond %{DOCUMENT_ROOT}$1.html -f
RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI}index.html !-f
RewriteRule ^(.+)/$ $1 [R=301,L]

RewriteCond %{REQUEST_URI} !\.html$
RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI}.html -f
RewriteRule ^(.*[^/])$ $1.html [L]
```
