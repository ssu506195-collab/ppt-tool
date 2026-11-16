"""Validate content and actual generated URLs, including fragment targets."""
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from pathlib import Path
import xml.etree.ElementTree as ET
from build import ROOT, OUT, load_content

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__()
        self.links=[]; self.ids=set(); self.lang=False; self.h1=0
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')=='zh-Hant'
        if tag=='h1': self.h1+=1
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate HTML id'
            self.ids.add(a['id'])
        for k in ['href','src']:
            if a.get(k): self.links.append(a[k])
        if tag=='img': assert a.get('alt'), 'Missing image alt'

def check():
    _,articles=load_content()
    diagrams=list((ROOT/'assets'/'diagrams').glob('*.svg'))
    for diagram in diagrams:
        assert ET.parse(diagram).getroot().tag.endswith('svg'), 'Invalid SVG'
    print(f'PASS: {len(diagrams)} educational SVG documents parse correctly.')
    pages={p:Page(p.read_text(encoding='utf-8')) for p in OUT.rglob('*.html')}
    links=0
    for path,page in pages.items():
        assert page.lang and page.h1==1, f'{path}: language or h1'
        for url in page.links:
            u=urlsplit(url)
            if u.scheme or u.netloc: continue
            assert not u.path.startswith('/'), f'{path}: root URL breaks repository hosting'
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            assert target.is_relative_to(OUT.resolve()), f'{path}: escaped output'
            assert target.is_file(), f'{path}: broken URL {url}'
            if u.fragment and target.suffix=='.html':
                assert unquote(u.fragment) in pages[target].ids, f'{path}: broken anchor {url}'
            links+=1
    for a in articles:
        assert (OUT/'articles'/f'{a["slug"]}.html').is_file()
    assert (OUT/'AGENTS.md').read_bytes()==(ROOT/'AGENTS.md').read_bytes()
    assert (OUT/'.nojekyll').is_file()
    print(f'PASS: {len(articles)} article schemas, {len(pages)} HTML pages, {links} local URLs, image alt text, headings and AGENTS.md copy.')
    print('External source availability and ANSYS simulation results require separate verification.')

if __name__=='__main__': check()
