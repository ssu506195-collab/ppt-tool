"""Reusable visual teaching components; content remains in JSON."""
from html import escape as e
import re
def rich(value):
    value=e(str(value),quote=True)
    value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
    value=re.sub(r'==(.+?)==',r'<mark>\1</mark>',value)
    return value
def modes(prefix='',compact=False):
    options=[('bend1','一階彎曲'),('side','側向彎曲'),('bend2','二階彎曲'),('bend3','三階彎曲'),('torsion','扭轉概念')]
    buttons=''.join('<button type="button" class="mode-tab'+(' active' if i==0 else '')+'" data-mode="'+key+'" aria-pressed="'+('true' if i==0 else 'false')+'"><span>'+chr(65+i)+'</span>'+label+'</button>' for i,(key,label) in enumerate(options))
    return f'''<div class="mode-explorer {'compact-explorer' if compact else ''}" data-mode-explorer>
    <div class="explorer-heading"><div><span class="eyebrow">PLAY WITH A MODE SHAPE</span><h3>同一支樑，可以怎麼振？</h3></div><span class="sticker">教學示意</span></div>
    <div class="mode-tabs" role="group" aria-label="選擇振型示意">{buttons}</div>
    <div class="mode-stage"><img class="mode-fallback" src="{prefix}assets/diagrams/bend1.svg" alt="一階彎曲的靜態示意，固定端不動、自由端位移較大。"><svg data-mode-svg viewBox="0 0 800 340" role="img" aria-label="一階彎曲振型示意" hidden></svg></div>
    <div class="mode-legend"><span><i class="ghost-line"></i>未變形中心線</span><span><i class="node-dot"></i>內部節點（中心線）</span><span class="color-key">相對位移 0 <i></i> 1</span></div>
    <div class="mode-insight" aria-live="polite"><b data-mode-name>一階彎曲 · Z 向</b><p data-mode-description>整支樑往同一方向彎。除了固定端，沒有其他內部節點。</p></div>
    <div class="mode-controls"><button type="button" class="play-button" data-mode-play aria-pressed="false">▶ 播放</button><label>展示倍率 <input data-mode-amplitude type="range" min="0.4" max="1.4" value="1" step="0.1" aria-label="展示倍率"><output data-amplitude-output>1.0×</output></label><label>相位 <input data-mode-phase type="range" min="0" max="360" step="1" value="90" aria-label="動畫相位"><output data-phase-output>90°</output></label></div>
    <p class="diagram-note">彎曲依 Euler–Bernoulli 梁理論繪製；扭轉為概念插值。動畫放大、同速慢放，顏色依各型態最大位移正規化；<strong>不是 ANSYS 求解結果，也不是實際三維階數排序。</strong> <a href="{prefix}articles/modal-basics.html#sources">圖解依據 ↗</a></p>
    </div>'''
def render_visual(b,prefix):
    t=b['type']
    if t=='modes':return modes(prefix)
    if t=='spotlight':
        return '<aside class="spotlight"><span class="spotlight-icon" aria-hidden="true">✦</span><div><span class="eyebrow">'+rich(b.get('label','一句話先懂'))+'</span><p>'+rich(b['text'])+'</p></div></aside>'
    if t=='figure':
        return '<figure class="teaching-figure"><div class="figure-label"><span>圖解</span><b>'+rich(b['title'])+'</b></div><a class="figure-zoom" data-figure-zoom data-figure-title="'+e(b['title'],quote=True)+'" href="'+prefix+e(b['src'],quote=True)+'"><img loading="lazy" src="'+prefix+e(b['src'],quote=True)+'" alt="'+e(b['alt'],quote=True)+'"><span>⤢ 放大圖解</span></a><figcaption>'+rich(b['caption'])+'</figcaption></figure>'
    if t=='compare':
        return '<div class="compare-grid">'+''.join('<div class="compare-card tone-'+str(i%4)+'"><span class="compare-number">'+str(i+1).zfill(2)+'</span><h3>'+rich(x['title'])+'</h3><p>'+rich(x['text'])+'</p></div>' for i,x in enumerate(b['items']))+'</div>'
    if t in ('details','checkpoint'):
        return '<details class="'+('checkpoint' if t=='checkpoint' else 'deep-dive')+'"><summary>'+('💡 ' if t=='checkpoint' else '＋ ')+rich(b['title'])+'</summary><div>'+''.join('<p>'+rich(x)+'</p>' for x in b['items'])+'</div></details>'
    return None
def home_hero(prefix=''):
    return '''<section class="hero playful-hero"><div class="hero-copy"><span class="eyebrow">ANSYS LAB NOTES / 圖解學習站</span><div class="hero-pin">第一站・模態分析</div><h1>原來，結構會<br><mark>這樣振！</mark><span class="spark">✳</span></h1><p>先看看它怎麼動，再弄懂為什麼。<br>把觀念、操作與排錯，變成看得懂、玩得動的實驗室筆記。</p><div class="hero-buttons"><a class="primary-button" href="articles/modal-basics.html">開始圖解入門 <span>↗</span></a><a class="outline-button" href="#try-it">先玩振型示意 ↓</a></div><div class="hero-meta">WORKBENCH 2024 R2 · 英文選項 ＋ 中文說明</div></div><div class="hero-visual notebook-visual"><span class="tape"></span><div class="visual-label"><span>HOW DOES IT MOVE?</span><span>看圖先懂一點點</span></div><img src="assets/diagrams/bend-vs-twist.svg" alt="彎曲與扭轉兩種不同的振動形狀示意。"><div class="visual-caption"><span>彎起來？扭過去？每種姿勢都值得看懂。</span></div></div></section>'''
