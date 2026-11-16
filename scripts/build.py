"""Build a portable, dependency-free multi-page learning site."""
from pathlib import Path
from html import escape as e
import json
import re
import shutil
from visuals import render_visual, rich, modes, home_hero
from make_diagrams import make as make_diagrams
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
KINDS = {'concept': '觀念筆記', 'tutorial': '操作教學', 'troubleshooting': '問題紀錄'}
REQUIRED = {
    'concept': ['學習目標', '核心觀念', '範例', '常見誤解', '重點整理'],
    'tutorial': ['學習目標', '前置條件', '案例參數', '操作步驟', '結果檢查', '重點整理'],
    'troubleshooting': ['問題現象', '適用情境', '檢查順序', '處理方式', '完成條件', '重點整理']}
SLUG = re.compile(r'^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$')

def load_content():
    modules = json.loads((ROOT / 'content/modules.json').read_text(encoding='utf-8'))
    articles = []
    for path in sorted((ROOT / 'content/articles').glob('*.json')):
        a = json.loads(path.read_text(encoding='utf-8'))
        for key in ['slug','category','kind','title','summary','version','level','minutes','updated','verification','prerequisites','tags','sections','sources','related']:
            assert key in a, f'{path.name}: missing {key}'
        assert SLUG.fullmatch(a['slug']) and path.stem == a['slug'], f'{path}: invalid slug'
        assert a['category'] in [m['id'] for m in modules], f'{path}: category'
        assert a['kind'] in KINDS, f'{path}: kind'
        assert a['version'] == '2024 R2', f'{path}: unsupported version'
        assert isinstance(a['minutes'], int) and a['minutes'] > 0
        date.fromisoformat(a['updated'])
        assert a['verification'] in ['文件查證／待實機驗證','實機驗證']
        if a['verification'] == '實機驗證':
            assert a.get('tested_by') and a.get('tested_on') and a.get('evidence')
            date.fromisoformat(a['tested_on'])
            for evidence in a['evidence']:
                ep = (ROOT / evidence).resolve()
                assert ep.is_relative_to((ROOT / 'assets').resolve()) and ep.is_file(), 'Invalid evidence'
        titles = ' '.join(s['title'] for s in a['sections'])
        assert all(t in titles for t in REQUIRED[a['kind']]), f'{path}: required sections'
        assert len({s['id'] for s in a['sections']}) == len(a['sections'])
        assert all(SLUG.fullmatch(s['id']) for s in a['sections'])
        assert a['sources'], f'{path}: missing sources'
        for src in a['sources']:
            assert all(src.get(k) for k in ['title','url','version','support'])
            assert src['url'].startswith('https://')
        for section in a['sections']:
            for block_item in section['blocks']:
                if block_item['type']=='figure':
                    assert all(block_item.get(k) for k in ['src','title','alt','caption'])
                    figure_path=(ROOT/block_item['src']).resolve()
                    assert figure_path.is_relative_to((ROOT/'assets').resolve()) and figure_path.is_file(), 'Missing figure'
        assert any(b['type'] in ['figure','modes','beam'] for section in a['sections'] for b in section['blocks']), 'Every article needs a relevant visual'
        articles.append(a)
    ids = {a['slug'] for a in articles}
    for a in articles:
        assert all(r in ids and r != a['slug'] for r in a['related']), f'{a["slug"]}: broken related'
    order = {'modal-basics':0,'modal-cantilever':1,'modal-zero-frequency':2,'modal-mesh-check':3}
    return modules, sorted(articles,key=lambda a: order.get(a['slug'],100))

def txt(value):
    return e(str(value), quote=True)

def article_url(a):
    return 'articles/' + a['slug'] + '.html'

def card(a, prefix='', index=1):
    previews={'modal-basics':'bend-vs-twist','modal-cantilever':'fixed-face','modal-zero-frequency':'rigid-vs-elastic','modal-mesh-check':'mesh-study'}
    preview=previews.get(a['slug'],'workflow')
    return f'''<a class="article-card" href="{prefix}{article_url(a)}" data-kind="{a['kind']}" data-search="{txt(' '.join([a['title'],a['summary'],*a['tags']]))}">
    <div class="card-top"><span class="badge {a['kind']}">{KINDS[a['kind']]}</span><span class="card-number">{index:02d}</span></div>
    <img class="card-illustration" loading="lazy" src="{prefix}assets/diagrams/{preview}.svg" alt="{txt(a['title'])}的教學圖解"><h3>{txt(a['title'])}</h3><p>{txt(a['summary'])}</p><div class="card-bottom"><span>{a['minutes']} 分鐘 · {txt(a['level'])}</span><span class="card-check" data-status="{a['slug']}">開始閱讀 ↗</span></div></a>'''

def shell(title, body, modules, active='home', prefix='', toc='', page=''):
    links = ''.join(f'<a class="module-link {"selected" if active == m["id"] else ""}" href="{prefix}modules/{m["id"]}.html"><span class="module-icon">{i:02d}</span><span>{txt(m["name"])}<small>{txt(m["tool"])}</small></span>{"<span class=mini>規劃中</span>" if not m["ready"] else ""}</a>' for i,m in enumerate(modules,1))
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="實驗室 ANSYS 學習與問題整理站。Workbench 2024 R2，英文介面搭配繁體中文說明。"><title>{txt(title)} | ANSYS Lab Notes</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/playful.css"><script defer src="{prefix}assets/modal-math.js"></script><script defer src="{prefix}assets/modes.js"></script><script defer src="{prefix}assets/app.js"></script></head>
    <body data-page="{txt(page)}"><a class="skip" href="#main">跳到主要內容</a><div class="shade" data-close-menu></div>
    <aside class="sidebar" id="navigation" aria-label="主要導覽"><a class="brand" href="{prefix}index.html"><span class="brand-mark">∿</span><span>ANSYS<small>LAB NOTES / 實驗室筆記</small></span></a><p class="sidebar-intro">從「看懂怎麼動」，<br>到「自己做得出來」。</p><a class="home-link {"selected" if active == "home" else ""}" href="{prefix}index.html">⌂　學習總覽</a><div class="nav-label">模擬主題</div>{links}<div class="nav-label">一起留下筆記</div><a class="contribute-link {"selected" if active == "contribute" else ""}" href="{prefix}contribute.html">＋　新增與維護內容</a><a class="contribute-link" href="{prefix}AGENTS.md">↗　閱讀 AGENTS.md</a><div class="side-footer"><span class="dot"></span> 2024 R2 · EN / 繁中說明<br><small>學習紀錄，持續累積。</small></div></aside>
    <div class="workspace"><header class="topbar"><div><button class="menu-button" aria-label="開啟導覽" aria-expanded="false" aria-controls="navigation">☰</button><a href="{prefix}index.html">實驗室學習站</a><span class="slash">/</span><span>{txt(title)}</span></div><span class="version-pill">WORKBENCH 2024 R2</span></header><main id="main" tabindex="-1">{body}</main><footer class="footer"><span>ANSYS LAB NOTES · 從理解到重現</span><span>獨立學習整理 · 非 ANSYS 官方教材</span></footer></div>{toc}</body></html>'''

def block(b,prefix):
    t = b['type']
    visual = render_visual(b,prefix)
    if visual is not None: return visual
    if t == 'p': return '<p>' + rich(b['text']) + '</p>'
    if t == 'list': return '<ul>' + ''.join('<li>'+rich(x)+'</li>' for x in b['items']) + '</ul>'
    if t == 'formula': return '<div class="formula">'+rich(b['text'])+'</div>'
    if t == 'note': return '<aside class="note"><strong>'+rich(b['title'])+'</strong><p>'+rich(b['text'])+'</p></aside>'
    if t == 'steps': return '<ol class="steps">'+''.join('<li><h3>'+rich(x['title'])+'</h3><p>'+rich(x['text'])+'</p></li>' for x in b['items'])+'</ol>'
    if t == 'table':
        assert all(len(r)==len(b['headers']) for r in b['rows']), 'Mismatched table row'
        return '<div class="table-wrap" tabindex="0" role="region" aria-label="可水平捲動的資料表"><table><thead><tr>'+''.join('<th scope="col">'+txt(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(x)+'</td>' for x in r)+'</tr>' for r in b['rows'])+'</tbody></table></div>'
    if t == 'beam': return '<figure><img src="'+prefix+'assets/beam.svg" alt="一端固定的長方形懸臂樑；長 200、寬 20、厚 10 毫米。"><figcaption>原創幾何與變形方向示意，非 ANSYS 求解結果。</figcaption></figure>'
    raise ValueError('Unknown block type: '+t)

def write(path,html):
    dest=OUT/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding='utf-8')

def build():
    make_diagrams()
    modules,articles=load_content()
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    for f in ['AGENTS.md','README.md']:
        shutil.copy2(ROOT/f,OUT/f)
    (OUT/'.nojekyll').touch()
    # Remove stale generated article/module pages only; source and assets remain untouched.
    expected={OUT/article_url(a) for a in articles}|{OUT/'modules'/f'{m["id"]}.html' for m in modules}
    for folder in ['articles','modules']:
        for f in (OUT/folder).glob('*.html'):
            if f not in expected: f.unlink()
    n=len(articles)
    ready_count=sum(bool(m['ready']) for m in modules)
    cards=''.join(card(a,index=i) for i,a in enumerate(articles,1))
    module_tiles=''.join(f'<a class="module-tile" href="modules/{m["id"]}.html"><span>{txt(m["tool"])}</span><h3>{txt(m["name"])}</h3><p>{"已收錄 "+str(sum(a["category"]==m["id"] for a in articles))+" 篇" if m["ready"] else "規劃中 · 查看學習方向"}</p><b>↗</b></a>' for m in modules)
    home=f'''<section class="hero"><div class="hero-copy"><span class="eyebrow">THE LAB NOTEBOOK / VOL. 01</span><h1>模擬的每一步，<br>都有跡可循<span>。</span></h1><p>從第一個固有頻率，到可以交接的分析流程。<br>把觀念、操作與排錯，整理成下一個人也能接續的筆記。</p><a class="primary-button" href="articles/modal-basics.html">從模態分析開始 <span>↗</span></a><div class="hero-meta">ENGLISH INTERFACE <span>＋</span> 繁體中文說明</div></div><div class="hero-visual"><div class="visual-label"><span>CASE 001 / CANTILEVER</span><span>GEOMETRY STUDY</span></div><img src="assets/beam.svg" alt="懸臂樑幾何示意，一端固定；非模擬結果。"><div class="visual-caption"><span>單一實體 → 固定端 → 前六階振型</span><span>示意圖</span></div></div></section>
    <div class="stats-strip"><div><b>{ready_count:02d}</b><span>目前開放主題</span></div><div><b>{n:02d}</b><span>入門學習筆記</span></div><div><b>2024 R2</b><span>教學基準版本</span></div><div class="progress-stat"><b id="reading-count">0 / {n}</b><span>本機已讀進度</span></div></div>
    <section class="content-section"><div class="section-heading"><div><span class="eyebrow">YOUR LEARNING PATH</span><h2>從這裡，開始第一個分析</h2></div><a class="text-link" href="modules/modal.html">模態分析專區 ↗</a></div><div class="learning-path"><a href="articles/modal-basics.html"><span>01 / 理解</span><strong>先掌握基本觀念</strong><small>頻率、振型與分析假設</small></a><a href="articles/modal-cantilever.html"><span>02 / 實作</span><strong>跟著完成懸臂樑</strong><small>材料、網格、拘束與求解</small></a><a href="articles/modal-zero-frequency.html"><span>03 / 檢查</span><strong>學會判讀與排錯</strong><small>近零頻率與連通性檢查</small></a></div></section>
    <section class="content-section" id="library"><div class="section-heading"><div><span class="eyebrow">KNOWLEDGE LIBRARY</span><h2>每一篇，都讓下一步更清楚</h2></div></div><div class="library-tools"><div class="filter-group" role="group" aria-label="文章類型篩選"><button class="filter active" data-filter="all" aria-pressed="true">全部筆記</button><button class="filter" data-filter="concept" aria-pressed="false">觀念筆記</button><button class="filter" data-filter="tutorial" aria-pressed="false">操作教學</button><button class="filter" data-filter="troubleshooting" aria-pressed="false">問題紀錄</button></div><label class="search-box"><span aria-hidden="true">⌕</span><input id="article-search" type="search" placeholder="搜尋頻率、固定支撐…" aria-label="搜尋文章標題、摘要與標籤"></label></div><p class="search-status" aria-live="polite" id="search-status">共 {n} 篇筆記</p><div class="article-grid">{cards}</div><p class="empty-state" hidden>找不到符合的筆記，試試其他關鍵詞或類型。</p></section>
    <section class="content-section"><div class="section-heading"><div><span class="eyebrow">GROW WITH THE LAB</span><h2>一套方法，接續不同模擬</h2></div></div><div class="module-grid">{module_tiles}</div></section><section class="contribute-banner"><div><span class="eyebrow">WRITE IT ONCE. PASS IT ON.</span><h2>讓下一位學弟妹，少繞一點路。</h2><p>文章格式、查證方式與開發流程，都寫進 AGENTS.md。</p></div><a class="light-button" href="contribute.html">了解如何新增內容 ↗</a></section>'''
    hero_end=home.index('</section>')+len('</section>')
    home=home_hero()+home[hero_end:]
    marker='<section class="content-section"><div class="section-heading"><div><span class="eyebrow">YOUR LEARNING PATH'
    pos=home.index(marker)
    try_section='<section class="content-section try-section" id="try-it"><div class="section-heading"><div><span class="eyebrow">先玩再懂 / VIBRATION PLAYGROUND</span><h2>點一下，認識它的不同振動姿勢</h2></div></div>'+modes()+'</section>'
    home=home[:pos]+try_section+home[pos:]
    write(Path('index.html'),shell('學習總覽',home,modules))
    for m in modules:
        collection=[a for a in articles if a['category']==m['id']]
        content=f'<section class="page-heading"><span class="eyebrow">SIMULATION MODULE / {txt(m["tool"].upper())}</span><h1>{txt(m["name"])}</h1><p>{txt(m["desc"])}</p><div class="tag-row"><span class="badge">2024 R2</span><span class="badge">{len(collection)} 篇筆記</span></div></section>'
        if collection:
            content+='<div class="note"><strong>建議閱讀順序</strong><p>先讀基本觀念，再完成懸臂樑操作，接著練習近零頻率排查與網格檢查。操作文章目前為文件查證，等待實機驗證。你也可以先在首頁試玩不同振型示意。</p></div><div class="article-grid">'+''.join(card(a,'../',i) for i,a in enumerate(collection,1))+'</div>'
        else:
            content+='<div class="planning"><span class="eyebrow">COMING NEXT</span><h2>這個專區，留給下一次學習。</h2><p>尚未收錄操作教學。未來將沿用相同文章模板、英文選項搭配中文說明，以及來源與驗證紀錄。</p><a class="primary-button" href="../contribute.html">查看新增內容方式 ↗</a></div>'
        write(Path('modules')/(m['id']+'.html'),shell(m['name'],content,modules,m['id'],'../'))
    for a in articles:
        module_name=next(m['name'] for m in modules if m['id']==a['category'])
        pre='<ul>'+''.join('<li>'+txt(x)+'</li>' for x in a['prerequisites'])+'</ul>'
        sections=''.join('<section id="'+s['id']+'"><h2>'+txt(s['title'])+'</h2>'+''.join(block(b,'../') for b in s['blocks'])+'</section>' for s in a['sections'])
        sources='<ol class="source-list">'+''.join('<li><a target="_blank" rel="noopener noreferrer" href="'+txt(s['url'])+'">'+txt(s['title'])+' ↗</a><small>'+txt(s['version'])+' · '+txt(s['support'])+'</small></li>' for s in a['sources'])+'</ol>'
        related=''.join(card(next(x for x in articles if x['slug']==r),'../',i) for i,r in enumerate(a['related'],1))
        toc='<nav class="article-toc" aria-label="本頁目錄"><strong>這一頁的重點</strong><a href="#prerequisites">開始前</a>'+''.join('<a href="#'+s['id']+'">'+txt(s['title'])+'</a>' for s in a['sections'])+'<a href="#sources">參考來源</a></nav>'
        body=f'''<div class="article-layout"><article class="article-body"><a class="back-link" href="../modules/{a['category']}.html">← 返回模態分析專區</a><div class="tag-row"><span class="badge {a['kind']}">{KINDS[a['kind']]}</span><span class="badge">{txt(a['version'])}</span></div><h1>{txt(a['title'])}</h1><p class="article-lead">{txt(a['summary'])}</p><div class="article-meta">{a['minutes']} 分鐘 · {txt(a['level'])} <span>更新 {a['updated']}</span></div><div class="verification"><span class="dot"></span>{txt(a['verification'])}</div><div class="article-actions"><button class="primary-button mark-read" data-slug="{a['slug']}" aria-pressed="false">標記為已讀</button><button class="outline-button" data-print>列印／另存 PDF</button></div><section id="prerequisites"><h2>開始前</h2>{pre}</section>{sections}<section id="sources"><h2>參考來源</h2><p class="muted">以下來源用於技術查證；案例尺寸與初始網格是本教學自訂設定。原廠頁面可能依存取權限要求登入。</p>{sources}</section><section class="related"><h2>接著閱讀</h2><div class="article-grid">{related}</div></section></article>{toc}</div>'''
        body=body.replace('返回模態分析專區','返回'+txt(module_name)+'專區')
        write(Path('articles')/(a['slug']+'.html'),shell(a['title'],body,modules,a['category'],'../',page=a['slug']))
    contribute='''<article class="article-body contribute-page"><span class="eyebrow">THE PLAYBOOK</span><h1>把學到的，變成可以接續的。</h1><p class="article-lead">AGENTS.md 是給 AI 的專案規則，讓新增內容沿用同一套格式、查證方式與版型。</p><a class="primary-button" href="AGENTS.md">閱讀完整 AGENTS.md ↗</a><section><h2>同一套規則，三種文章</h2><div class="table-wrap"><table><thead><tr><th>觀念筆記</th><th>操作教學</th><th>問題紀錄</th></tr></thead><tbody><tr><td>學習目標 → 核心觀念 → 範例 → 常見誤解 → 重點整理</td><td>學習目標 → 前置條件 → 案例參數 → 操作步驟 → 結果檢查 → 重點整理</td><td>問題現象 → 適用情境 → 檢查順序 → 處理方式 → 完成條件 → 重點整理</td></tr></tbody></table></div></section><section><h2>讓 AI 新增一篇文章</h2><p>下載完整專案後，在 AI 編碼工具中開啟資料夾，先讓它閱讀根目錄的 AGENTS.md，再提出具體內容需求。例如：</p><div class="prompt-example">請先閱讀 AGENTS.md 與 content/schema.md，新增一篇「模態分析的網格檢查」觀念筆記。以 Workbench 2024 R2 為準，英文選項附中文名稱，引用官方文件；未執行的網格比較必須標記為待驗證。完成後執行生成與檢查，更新變更紀錄。</div></section><section><h2>新增流程</h2><ol class="steps"><li><h3>填寫文章模板</h3><p>複製 templates/article.json 到 content/articles/，使用英文小寫連字號檔名，依 content/schema.md 填妥欄位。</p></li><li><h3>重新生成網站</h3><p>執行 python scripts/build.py。首頁、分類頁、文章頁與搜尋用資料會同步更新；不需要手動製作每一頁的導覽。</p></li><li><h3>檢查與交接</h3><p>執行 python scripts/check.py，再檢查桌面與手機頁面。來源與 docs/ 一起提交 GitHub，並更新 CHANGELOG.md。</p></li></ol></section><section><h2>什麼可以寫成「已驗證」？</h2><p>閱讀官方文件，代表文件查證；完成 ANSYS 操作並留下版本、操作者、日期與實際結果證據，才可標示實機驗證。網站檢查成功與模擬結果正確，是兩種不同的檢查。</p></section><section><h2>延伸到其他軟體</h2><p>先在 content/modules.json 宣告新分類，再新增對應文章。沿用相同欄位與視覺規則，同時交代各軟體特有的假設、操作環境與結果檢查方式。</p></section></article>'''
    write(Path('contribute.html'),shell('新增與維護內容',contribute,modules,'contribute'))
    print(f'Built {len(articles)} articles, {len(modules)} module pages and 2 overview pages in docs/')

if __name__=='__main__': build()
