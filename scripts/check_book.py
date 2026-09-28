"""Check the deployed artifact: internal links, fragments, art and safe downloads."""
from html.parser import HTMLParser
import json
from pathlib import Path
import tarfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.images, self.ids = [], [], set()
        self.duplicates = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.duplicates.append(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'img':
            self.images.append(attrs)
        if tag in {'script', 'link'}:
            value = attrs.get('src') or attrs.get('href')
            if value:
                self.links.append(value)


def check():
    pages = json.loads((ROOT / 'book/pages.json').read_text())
    errors = []
    parsed = {}
    for path in SITE.glob('*.html'):
        text = path.read_text()
        parsed[path.name] = Page(text)
        if '{{' in text:
            errors.append(f'{path.name}: unresolved template token')
    for page in pages:
        name = page['slug'] + '.html'
        if name not in parsed:
            errors.append(f'Missing page {name}')
            continue
        document = parsed[name]
        if document.duplicates:
            errors.append(f'{name}: duplicate IDs {document.duplicates}')
        expected = {f'assets/images/{page["slug"]}-{kind}.png' for kind in ['guide', 'scene']}
        if not expected.issubset({img.get('src') for img in document.images}):
            errors.append(f'{name}: missing the two page-specific illustrations')
        for img in document.images:
            if not img.get('alt', '').strip():
                errors.append(f'{name}: image has no descriptive alternative')
        for value in document.links + [i.get('src', '') for i in document.images]:
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                errors.append(f'{name}: root-relative URL breaks project Pages: {value}')
            target = SITE / unquote(url.path) if url.path else SITE / name
            if not target.exists():
                errors.append(f'{name}: broken local link {value}')
            if target.suffix == '.html' and url.fragment:
                destination = parsed.get(target.name)
                if destination and unquote(url.fragment) not in destination.ids:
                    errors.append(f'{name}: missing fragment {value}')
    if len(list((SITE / 'assets/images').glob('*.png'))) != 24:
        errors.append('Expected exactly 24 original illustrations')
    for path in (SITE / 'downloads').glob('*.tar'):
        with tarfile.open(path) as archive:
            for member in archive.getmembers():
                components = Path(member.name).parts
                if member.name.startswith('/') or '..' in components or any(
                    p in {'.git', '.venv', '.env', 'node_modules'} for p in components
                ) or member.issym() or member.islnk():
                    errors.append(f'Unsafe archive member: {path.name}:{member.name}')
    index = json.loads((SITE / 'search.json').read_text())
    if len(index) != len(pages) or any(not (SITE / row['url']).is_file() for row in index):
        errors.append('Search index does not match the book')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} pages, 24 images, links/fragments, search index and download safety')


if __name__ == '__main__':
    check()
