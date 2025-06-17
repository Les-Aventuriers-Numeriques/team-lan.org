from pelican import signals, Pelican
from typing import List
from glob import glob
import htmlmin
import os
import re


def minify_sitemap(sender: Pelican, filename) -> None:
    try:
        with open(os.path.join(sender.settings.get('OUTPUT_PATH'), filename), 'r+', encoding='utf-8') as f:
            content = f.read()

            f.seek(0)
            f.write(htmlmin.minify(content, remove_optional_attribute_quotes=False, remove_empty_space=True, remove_comments=True))
            f.truncate()
    except FileNotFoundError:
        pass


def make_url_seo_friendly(sender: Pelican, filenames: List[str]) -> None:
    base_url = re.escape(sender.settings.get('SITEURL').removesuffix('/'))

    index_urls_regex = re.compile(fr'({base_url}\S*/)index\.html')
    page_urls_regex = re.compile(fr'({base_url}\S*)\.html')

    for filename in filenames:
        try:
            with open(os.path.join(sender.settings.get('OUTPUT_PATH'), filename), 'r+', encoding='utf-8') as f:
                count = 0

                (content, nsub) = index_urls_regex.subn(r'\1', f.read())

                count += nsub

                (content, nsub) = page_urls_regex.subn(r'\1', content)

                count += nsub

                if count == 0:
                    continue

                f.seek(0)
                f.write(content)
                f.truncate()
        except FileNotFoundError:
            pass


def finalized(sender: Pelican) -> None:
    filenames = []

    for extension in ('rss', 'atom', 'xml', 'html'):
        filenames.extend(glob(
            f'**/*.{extension}',
            root_dir=sender.settings.get('OUTPUT_PATH'),
            recursive=True
        ))

    make_url_seo_friendly(sender, filenames)
    minify_sitemap(sender, 'sitemap.xml')


def register():
    signals.finalized.connect(finalized)
