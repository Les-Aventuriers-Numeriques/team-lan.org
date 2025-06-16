from pelican import signals
import htmlmin
import os


def finalized(sender):
    # Minification de sitemap.xml + suppression suffixes .html
    try:
        with open(os.path.join(sender.output_path, 'sitemap.xml'), 'r+', encoding='utf-8') as f:
            content = f.read().replace('.html', '')

            f.seek(0)
            f.write(htmlmin.minify(content, remove_optional_attribute_quotes=False, remove_empty_space=True, remove_comments=True))
            f.truncate()
    except FileNotFoundError:
        pass


def register():
    signals.finalized.connect(finalized)
