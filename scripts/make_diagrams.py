"""Original, reproducible educational SVGs. No ANSYS solver results."""
from pathlib import Path
from html import escape
import math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'diagrams'
ROOTS=[1.875104068711961,4.694091132974175,7.854757438237613]
def shape(n,x):
    b=ROOTS[n-1];q=(math.cosh(b)+math.cos(b))/(math.sinh(b)+math.sin(b))
    def raw(t):return math.cosh(b*t)-math.cos(b*t)-q*(math.sinh(b*t)-math.sin(b*t))
    return raw(x)/abs(raw(1))
def project(x,y,z):return (112+520*x+.74*y,205+.42*y-z)
def point(kind,x,y,z,phase=1,amp=1):
    if kind=='torsion':
        th=.8*math.sin(math.pi*x/2)*phase*amp
        return project(x,y*math.cos(th)-z*math.sin(th),y*math.sin(th)+z*math.cos(th))
    n=2 if kind=='bend2' else 3 if kind=='bend3' else 1
    v=shape(n,x)*phase*amp
    return project(x,y+80*v if kind=='side' else y,z if kind=='side' else z+65*v)
def line(x1,y1,x2,y2,color='#789184',dash=''):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="2" {dash}/>'
def text(x,y,t,size=16,color='#244c3b',weight='500',anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(t)}</text>'
def rect(x,y,w,h,fill='#fffdf5',stroke='#b8cdbb',r=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
def svg(name,body,title,w=800,h=390):
    OUT.mkdir(parents=True,exist_ok=True)
    result=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">原創教學示意，非 ANSYS 求解結果。{escape(title)}</desc><defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1" fill="#dce3d7"/></pattern><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 0V7" stroke="#879e8d" stroke-width="2"/></pattern><linearGradient id="legend"><stop stop-color="#81bfe1"/><stop offset=".5" stop-color="#b9d4a0"/><stop offset="1" stop-color="#ed9c69"/></linearGradient></defs><rect width="{w}" height="{h}" rx="20" fill="#faf9f0"/><rect width="{w}" height="{h}" fill="url(#dots)" rx="20"/><g font-family="Microsoft JhengHei, sans-serif">{body}</g></svg>'
    (OUT/name).write_text(result,encoding='utf-8')
def poly(points,color,stroke='#3c6b58'):
    return f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in points)}" fill="{color}" stroke="{stroke}" stroke-width=".65" stroke-linejoin="round"/>'
def ribbon(kind='bend1',nseg=42):
    result='<rect x="75" y="158" width="22" height="94" fill="url(#hatch)" stroke="#708d79"/>'
    result+=line(105,205,657,205,'#a6b5a8','stroke-dasharray="6 6"')
    for i in range(nseg):
        xa=i/nseg;xb=(i+1)/nseg
        n=2 if kind=='bend2' else 3 if kind=='bend3' else 1
        magnitude=math.sin(math.pi*(xa+xb)/4) if kind=='torsion' else abs(shape(n,(xa+xb)/2))
        v=min(magnitude,1);colors=((129,191,225),(237,156,105));color='rgb('+','.join(str(round(colors[0][j]*(1-v)+colors[1][j]*v)) for j in range(3))+')'
        top=[point(kind,xa,-18,5),point(kind,xb,-18,5),point(kind,xb,18,5),point(kind,xa,18,5)]
        side=[point(kind,xa,18,5),point(kind,xb,18,5),point(kind,xb,18,-5),point(kind,xa,18,-5)]
        result+=poly(side,'#b8c9af')+poly(top,color)
    result+=text(38,283,'固定端',13)+text(625,283,'自由端',13)
    return result
def make():
    for kind,title in [('bend1','一階彎曲：同一方向彎起'),('side','側向彎曲：換一個方向'),('bend2','二階彎曲：出現一個內部節點'),('bend3','三階彎曲：出現兩個內部節點'),('torsion','扭轉概念：截面繞長軸轉動')]:
        svg(kind+'.svg',text(30,40,title,23,weight='700')+text(30,69,'彎曲採梁理論；扭轉為概念插值。顏色為相對位移示意。',12)+ribbon(kind)+text(30,350,'教學示意 · 放大顯示 · 不代表實際三維模態排序或受迫振幅',12),title)
    body=text(28,36,'同一支樑，可以有不同的「振動姿勢」',23,weight='700')
    for i,(kind,title,sub) in enumerate([('bend1','一階彎曲','沒有內部節點'),('bend2','二階彎曲','1 個內部節點'),('bend3','三階彎曲','2 個內部節點')]):
        y=70+i*220
        body+=rect(24,y,752,204,fill=['#eaf4fb','#fff0df','#f0eafa'][i])
        body+=text(45,y+33,title,20,weight='700')+text(570,y+32,sub,14)
        body+=f'<g transform="translate(0,{y-37}) scale(1,.72)">'+ribbon(kind)+'</g>'
    body+=text(28,775,'圖例不是 ANSYS 第 1～3 階排序；這裡只比較同方向的彎曲家族。',13)
    svg('mode-family.svg',body,'同方向前三個彎曲振型：依序有零、一、兩個內部節點',800,805)
    body=text(28,40,'先找它怎麼動，再判斷是哪種模態',23,weight='700')
    for i,(kind,title,tip) in enumerate([('bend1','彎曲','中心線彎曲，截面隨之移動'),('torsion','扭轉','截面繞樑的長軸旋轉')]):
        x=i*400
        body+=rect(x+18,75,364,250,fill='#eaf4fb' if i==0 else '#fff0df')
        body+=text(x+40,112,title,21,weight='700')
        body+=f'<g transform="translate({x-15},53) scale(.58,.85)">'+ribbon(kind)+'</g>'
        body+=text(x+40,302,tip,13)
    body+=text(28,365,'彎曲取自梁理論；扭轉為概念示意，不描述截面翹曲。',13)
    svg('bend-vs-twist.svg',body,'彎曲與扭轉的幾何差異')
    body=text(28,40,'固定端：選哪個面，真的有差！',23,weight='700')
    body+=ribbon('bend1')+text(28,88,'左側整個端面 → Fixed Support（固定支撐）',15,color='#aa5c32')
    body+=line(245,98,107,177,'#ca7143')+text(440,330,'其餘表面保持自由',15)
    body+=text(28,364,'尺寸 L = 200 mm、b = 20 mm、h = 10 mm；本圖只說明幾何與拘束。',12)
    svg('fixed-face.svg',body,'懸臂樑固定的是長度方向一端的完整端面')
    body=text(28,40,'剛體移動，和彈性彎曲，怎麼分？',23,weight='700')
    cards=[('整體平移','物件換位置，形狀沒變','#e8f3fa'),('彈性彎曲','相對位置改變，形狀會彎','#f0f4df'),('零件獨立漂動','檢查是否漏接或未拘束','#ffedde')]
    for i,(title,sub,color) in enumerate(cards):
        x=18+260*i;body+=rect(x,78,244,262,color)+text(x+17,115,title,18,weight='700')
        if i==0:
            body+=rect(x+30,178,155,20,'#d9e2d8',r=2)+rect(x+50,145,155,20,'#86bfd8',r=2)+text(x+180,167,'↗',27)
        elif i==1:
            body+=f'<g transform="translate({x-5},112) scale(.37,.5)">'+ribbon('bend1')+'</g>'
        else:
            body+=rect(x+25,173,80,23,'#a1c1a7',r=4)+rect(x+139,135,72,23,'#e9b17c',r=4)+line(x+111,184,x+145,153,'#c17147','stroke-dasharray="5 5"')
        body+=text(x+15,294,sub,12)
    body+=text(28,370,'自由—自由模型的剛體模態可能合理；有固定需求時才依實物修正。',12)
    svg('rigid-vs-elastic.svg',body,'比較剛體平移、彈性彎曲及未連接零件')
    body=text(28,40,'網格不是比誰密，是檢查結果是否穩定',23,weight='700')
    for i,(cols,rows,label) in enumerate([(6,2,'較粗網格'),(12,4,'中間網格'),(24,8,'較細網格')]):
        x=26+i*258;y=118;w=230;h=92
        body+=rect(x,y,w,h,['#e9f4fa','#eff4df','#fff0df'][i],r=1)
        for j in range(1,cols):body+=line(x+j*w/cols,y,x+j*w/cols,y+h,'#8fac9d')
        for j in range(1,rows):body+=line(x,y+j*h/rows,x+w,y+j*h/rows,'#8fac9d')
        body+=text(x,y-18,label,18,weight='700')+text(x,y+h+35,'頻率：待求解、待記錄',13)
    body+=rect(27,286,745,61,'#e9efdc')+text(47,322,'每次保持幾何、材料、拘束一致，並追蹤相同振型。',16)
    body+=text(28,375,'分割僅為概念示意；不代表指定元素類型、尺寸或已取得收斂結果。',12)
    svg('mesh-study.svg',body,'粗、中、細三種概念網格；不附虛構的收斂數據')
    body=text(28,40,'從輸入條件，到看懂輸出',23,weight='700')
    labels=[('01','Workbench','串接分析流程','#eaf3fa'),('02','DesignModeler','建立案例幾何','#fff0df'),('03','Mechanical','設定網格與拘束','#eff3df'),('04','Mechanical','查看頻率與振型','#f2eafb')]
    for i,(num,title,sub,color) in enumerate(labels):
        x=32+(i%2)*390;y=82+(i//2)*135
        body+=rect(x,y,346,108,color)+text(x+20,y+29,num,14,color='#7b846e')+text(x+20,y+60,title,22,weight='700')+text(x+20,y+87,sub,14)
    body+=text(28,376,'流程圖是學習導覽，不是 ANSYS 軟體畫面截圖。',12)
    svg('workflow.svg',body,'Workbench、DesignModeler 和 Mechanical 各自負責的工作')
    body=text(28,40,'看結果時，眼睛先去這三個地方',23,weight='700')
    body+=rect(22,77,258,250,'#eaf3fa')+text(42,112,'① 頻率與階數',19,weight='700')
    body+=text(42,149,'Mode（階數）   Frequency（頻率）',12)
    for i in range(3):body+=line(42,168+i*43,256,168+i*43,'#bfd1d7')+text(42,194+i*43,str(i+1),15)+text(134,194+i*43,'待求解',14)
    body+=rect(300,77,477,250,'#fff4df')+text(322,111,'② 振型與固定端',19,weight='700')
    body+=f'<g transform="translate(266,43) scale(.73,.9)">'+ribbon('bend2')+'</g>'
    body+=text(42,365,'③ 顏色讀相對位移；圖例、數值與頻率要以你自己的求解結果為準。',14)
    svg('read-results.svg',body,'結果閱讀示意：頻率、振型和相對位移；表格為待填欄位')
    body=text(28,40,'改變模型，就可能改變它的動態特徵',23,weight='700')
    for i,(title,sub,color) in enumerate([('幾何','長度、厚度、形狀','#eaf3fa'),('材料','剛性與質量','#fff0df'),('拘束','夾持方式與連接','#f0edfa')]):
        x=25+i*260;body+=rect(x,88,235,197,color)+text(x+20,132,title,26,weight='700')+text(x+20,168,sub,15)
        if i==0:body+=line(x+25,226,x+184,226,'#458273')+line(x+25,248,x+128,248,'#d08c5c')
        elif i==1:body+=f'<path d="M{x+25} 230h20l10-16 13 32 13-32 13 32 13-16h42" fill="none" stroke="#8d7353" stroke-width="3"/>'
        else:body+=f'<rect x="{x+28}" y="197" width="17" height="57" fill="url(#hatch)"/>'+rect(x+45,218,146,15,'#88ad96',r=2)
    body+=text(28,343,'所以比較兩個結果前，先確認輸入條件是否相同。',16)+text(28,375,'教學概念圖 · 不預測任意模型的實際頻率',12)
    svg('what-changes.svg',body,'幾何、材料與拘束共同影響模態結果')
    print('Generated 13 original teaching SVG diagrams.')
if __name__=='__main__':make()
