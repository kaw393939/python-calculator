"""Build the public learning book from reviewed Markdown, without a web service."""
import argparse
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

import markdown

ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / 'book/pages.json').read_text())
MAP = {(ROOT / page['source']).resolve(): page['slug'] + '.html'
       for page in PAGES if page['source']}


class LinkRewriter(HTMLParser):
    def __init__(self, source, output):
        super().__init__(convert_charrefs=False)
        self.source, self.output, self.parts = source, output, []

    def handle_starttag(self, tag, attrs):
        fixed = []
        for key, value in attrs:
            if key in {'href', 'src'} and value and not re.match(r'^(https?:|mailto:|#)', value):
                path, _, fragment = value.partition('#')
                target = (self.source.parent / path).resolve()
                if target in MAP:
                    value = MAP[target] + ('#' + fragment if fragment else '')
                elif target.is_dir():
                    value = 'downloads/b22b89f.tar'
                elif target.is_file() and target.is_relative_to(ROOT):
                    relative = target.relative_to(ROOT).as_posix().replace('/', '--')
                    destination = self.output / 'downloads' / relative
                    shutil.copyfile(target, destination)
                    value = 'downloads/' + relative
            fixed.append((key, value))
        self.parts.append('<' + tag + ''.join(' '+key+(f'="{escape(value, quote=True)}"'
                           if value is not None else '') for key, value in fixed) + '>')

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append('&' + name + ';')

    def handle_charref(self, name):
        self.parts.append('&#' + name + ';')


def guide(page, kind):
    title = 'Mira’s field note' if kind == 'tip' else 'Worth knowing'
    return f'''<aside class="guide-callout {kind}"><img src="assets/images/{page['slug']}-guide.png"
      alt="Mira, your illustrated engineering guide" loading="lazy" width="96" height="96">
      <div><span class="eyebrow">{title}</span><p>{escape(page[kind])}</p></div></aside>'''


def home():
    cards = ''.join(f'''<a class="chapter-card" href="{p['slug']}.html"><span class="chapter-number">0{i}</span>
      <h3>{escape(p['title'])}</h3><p>{escape(p['deck'])}</p><span class="card-link">Explore chapter ↗</span></a>'''
      for i, p in enumerate(PAGES[2:8], 1))
    return f'''<section class="promise-strip" aria-label="What you get"><div><strong>06</strong><span>hands-on chapters</span></div>
    <div><strong>01</strong><span>real project, end to end</span></div><div><strong>Your pace</strong><span>no sign-up, no gatekeeping</span></div></section>
    <section class="welcome-section"><div><span class="eyebrow">MEET YOUR GUIDE</span><h2>“The spark is yours.<br>I’ll help you shape it.”</h2>
    <p>I’m Mira, your illustrated companion through this book. Together, we’ll turn a rough idea into a calculator, a tested command-line tool, and a web experience.</p>
    <p>The real transformation? Becoming an engineer who can explain why their software works—and recognize when they haven’t proved it yet.</p>
    <a class="text-link" href="start.html">Let’s set up your workshop →</a></div>
    <img src="assets/images/home-guide.png" alt="Mira smiles and welcomes you with a glowing engineering notebook" width="600" height="600"></section>
    <section id="chapters"><div class="section-heading"><div><span class="eyebrow">YOUR PATH THROUGH THE BOOK</span><h2>Six chapters. A different way to build.</h2></div><p>Small steps. Real artifacts.<br>Evidence at every turn.</p></div><div class="chapter-grid">{cards}</div></section>
    <section class="begin-banner"><span class="eyebrow">MAKE YOUR FIRST SMALL COMMITMENT</span><h2>One clear requirement.<br>That’s where it begins.</h2><p>You don’t need to promise mastery today. Just give your next idea a testable definition of success.</p><a class="button" href="requirements.html">Write my first requirement <span>↗</span></a></section>
    <section class="resource-grid"><a href="glossary.html"><h3>Learn the language ↗</h3><p>Vocabulary connected to real code and common misconceptions.</p></a><a href="case-study.html"><h3>See the real journey ↗</h3><p>Follow the decisions, failures, and fixes behind the project.</p></a><a href="instructor.html"><h3>Teach this book ↗</h3><p>Session plans, a transparent rubric, and honest validation notes.</p></a></section>'''


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'downloads').mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'book/assets', output / 'assets', dirs_exist_ok=True)
    # Approved educational snapshots; never include .git, local CSVs or virtual environments.
    for revision in ['4ba5178', '6ae07a1', '56444fc', 'b22b89f']:
        subprocess.run(['git', 'archive', '--format=tar', f'--output={output}/downloads/{revision}.tar',
                        revision, 'src', 'tests', 'examples', 'pyproject.toml', 'README.md', 'docs',
                        '.gitignore', '.github'], cwd=ROOT, check=True)
    with tarfile.open(output / 'downloads/lesson-pack.tar', 'w') as bundle:
        for path in sorted((ROOT / 'docs/learning').rglob('*')):
            if path.is_file():
                bundle.add(path, arcname='learning/' + path.relative_to(ROOT / 'docs/learning').as_posix())
    template = (ROOT / 'book/templates/page.html').read_text()
    search = []
    for index, page in enumerate(PAGES):
        slug = page['slug']
        nav = ''.join(f'<a href="{p["slug"]}.html" '+('aria-current="page"' if p==page else '')+
                      f'>{escape(p["label"])}</a>' for p in PAGES)
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
        if page['source']:
            source = ROOT / page['source']
            text = re.sub(r'^# .+\n', '', source.read_text(), count=1)
            converted = md.convert(text)
            rewriter = LinkRewriter(source, output)
            rewriter.feed(converted)
            content = '<article class="prose" id="reading">' + ''.join(rewriter.parts) + '</article>'
            toc = md.toc
            if slug == 'start':
                content = '''<section class="download-box"><h2>Your workshop files</h2><p>The Git repository is private. These approved source snapshots let you follow the labs without repository access. Download the lesson pack to keep instructions beside your historical code copy.</p>''' + ''.join(
                    f'<a href="downloads/{rev}.tar" download>↓ {rev} source snapshot</a>' for rev in ['b22b89f', '4ba5178', '6ae07a1', '56444fc']) + '<a href="downloads/lesson-pack.tar" download>↓ Complete lesson pack</a></section>' + content
        else:
            text = page['deck']
            content, toc = home(), ''
        prev = PAGES[index - 1] if index else None
        next_page = PAGES[index + 1] if index < len(PAGES)-1 else PAGES[0]
        footer_nav = (f'<a href="{prev["slug"]}.html">← {escape(prev["label"])}</a>' if prev else '<span></span>')
        footer_nav += f'<a href="{next_page["slug"]}.html">{escape(next_page["label"])} →</a>'
        cta = '<div class="hero-actions"><a class="button" href="start.html">Begin your transformation <span>↗</span></a><a class="text-link" href="#chapters">Explore the chapters ↓</a></div>' if slug == 'home' else '<a class="text-link" href="#reading">Start reading ↓</a>'
        values = dict(title=escape(page['title']), slug=slug, label=escape(page['label']),
                      eyebrow=escape(page['eyebrow']), deck=escape(page['deck']), nav=nav,
                      content=content, tip=guide(page,'tip'), fact=guide(page,'fact'), toc=toc,
                      footer_nav=footer_nav, cta=cta,
                      image_alt=escape('Mira illustrates '+page['label'].lower()+' through an engineering scene'),
                      mark='' if slug=='home' else '<button class="button secondary" id="mark-read" hidden>Mark this page complete ✓</button>')
        rendered = template
        for key, value in values.items():
            rendered = rendered.replace('{{'+key+'}}', value)
        (output / (slug + '.html')).write_text(rendered)
        search.append({'title':page['label'],'url':slug+'.html','text':re.sub(r'[#*`|]', '', text)})
    shutil.copyfile(output / 'home.html', output / 'index.html')
    (output / 'search.json').write_text(json.dumps(search))
    (output / '.nojekyll').touch()
    print(f'Built {len(PAGES)} illustrated pages in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    build(args.output.resolve())
