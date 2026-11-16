"""Original multi-physics educational drawings, not solver outputs."""
from make_diagrams import svg,rect,text,line
import math
def arrow(x1,y1,x2,y2,color='#5b8e72'):
    angle=math.atan2(y2-y1,x2-x1);s=8
    return line(x1,y1,x2,y2,color)+f'<path d="M{x2-s*math.cos(angle-.45):.2f} {y2-s*math.sin(angle-.45):.2f}L{x2} {y2}L{x2-s*math.cos(angle+.45):.2f} {y2-s*math.sin(angle+.45):.2f}" fill="none" stroke="{color}" stroke-width="2"/>'
def make():
    body=text(28,40,'電位看高度，電場看空間變化',23,weight='700')
    for i in range(10):
        c=f'rgb({round(233-10*i)},{round(161+4*i)},{round(106+11*i)})'
        body+=rect(70,100+i*17,500,17,c,c,0)
    body+=rect(70,85,500,15,'#a96f4f',r=3)+rect(70,270,500,15,'#658aa8',r=3)
    for x in [110,190,270,350,430,510]:body+=arrow(x,123,x,250,'#436e57')
    body+=text(602,108,'上板 +V',17)+text(602,274,'下板 0 V',17)+text(603,191,'E ↓',23,weight='700')
    body+=text(70,330,'色帶：電位從高到低；箭頭：電場指向低電位。',16)
    body+=text(28,375,'理想均勻間隙解析示意；不含有限電極邊緣效應。',12)
    svg('maxwell-potential.svg',body,'理想平行板的電位色帶與向下電場')
    body=text(28,40,'上、下給電壓；左右保留零法向通量',23,weight='700')
    body+=rect(150,112,500,160,'#e9f3f8',r=0)+line(150,112,650,112,'#c47d4c')+line(150,272,650,272,'#689ab6')
    body+=text(200,92,'y = 10 mm：1000 V',18)+text(220,309,'y = 0：0 V',18)
    for x in [235,345,455,565]:body+=arrow(x,140,x,240)
    body+=text(17,180,'Neumann',13)+text(17,203,'不穿出',13)+text(665,180,'Neumann',13)+text(665,203,'不穿出',13)
    body+=text(256,355,'真空介質：40 × 10 mm',16)
    body+=text(28,382,'教學幾何示意；不是在有限銅板外包一個接地空氣盒。',11)
    svg('maxwell-boundaries.svg',body,'理想間隙的兩條電壓邊與兩條 Neumann 側邊')
    body=text(28,40,'尖角附近的峰值，要連幾何與網格一起看',23,weight='700')
    for i in range(2):
        x=25+i*390;body+=rect(x,80,360,250,'#fff0df' if i==0 else '#eaf3e4')
        body+=text(x+22,116,'理想尖角' if i==0 else '有限圓角',22,weight='700')
        d=f'M{x+55} 265V170H{x+165}L{x+230} 265Z' if i==0 else f'M{x+55} 265V170H{x+145}Q{x+170} 170 {x+184} 193L{x+230} 265Z'
        body+=f'<path d="{d}" fill="#a9c6af" stroke="#48795c" stroke-width="2"/>'
        for j in range(5):
            body+=f'<path d="M{x+160+j*16} 145Q{x+230+j*12} 165 {x+265+j*11} 232" fill="none" stroke="#c28d65" stroke-width="1.8"/>'
    body+=text(28,366,'線條只表達局部集中趨勢，不是計算場線；不據此判斷放電或場強數值。',12)
    svg('maxwell-corners.svg',body,'尖角與有限圓角的局部檢查概念')
    body=text(28,40,'兩個實體、一個間隙、明確的速度方向',23,weight='700')
    body+=rect(85,135,72,150,'#a4b89d',r=4)+rect(180,174,470,73,'#b7d5e6',r=4)
    body+=f'<rect x="62" y="132" width="19" height="156" fill="url(#hatch)" stroke="#7d9a7f"/>'
    body+=text(77,112,'固定背面',15)+text(91,317,'擋塊',16)+text(390,280,'運動方塊',17)
    body+=arrow(500,146,290,146,'#b96f46')+text(332,127,'VX = −1 m/s',18)
    body+=line(160,332,180,332,'#b96f46')+text(150,360,'間隙 1 mm',14)
    body+=text(28,382,'兩者皆為可變形線彈性實體；圖未按實際比例繪製。',11)
    svg('impact-setup.svg',body,'彈性方塊朝左撞擊背面固定的擋塊')
    body=text(28,40,'動能 ↔ 彈簧能：先看理想能量交換',23,weight='700')
    body+=line(90,298,710,298)+line(90,298,90,95)
    body+=text(56,107,'1',14)+text(56,301,'0',14)+text(250,343,'接觸歷程（正規化時間）',16)
    for energy,color in [('K','#649cbe'),('U','#ca8b59')]:
        pts=[]
        for i in range(101):
            t=i/100;v=math.cos(math.pi*t)**2 if energy=='K' else math.sin(math.pi*t)**2
            pts.append(f'{90+620*t:.2f},{298-185*v:.2f}')
        body+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="3"/>'
    body+=text(420,83,'藍：動能 K　橘：彈簧能 U',14)
    body+=line(90,113,710,113,'#8da47b','stroke-dasharray="5 5"')+text(110,96,'K + U = 起始動能',14)
    body+=text(28,382,'無阻尼單自由度模型的解析曲線，不是三維 LS-DYNA 結果。',11)
    svg('impact-energy.svg',body,'簡化彈簧接觸模型中的正規化動能與彈簧能')
    body=text(28,40,'求解很多小步，只存其中一些畫面',23,weight='700')
    for row,y in enumerate([145,245]):
        body+=line(70,y,730,y)
        for i in range(31):
            if row==0 or i%10==0:
                body+=f'<circle cx="{75+21*i}" cy="{y}" r="{4 if row==0 else 9}" fill="{"#87ae8d" if row==0 else "#d9a06b"}"/>'
        body+=text(70,y-25,'求解步（示意）' if row==0 else '輸出影格（示意）',18,weight='700')
    body+=text(70,320,'存得更密，才能看見更多歷程；但不等於求解步長變小。',16)
    body+=text(28,378,'時間尺度、點數與間距只是示意，不是通用求解參數。',12)
    svg('explicit-steps.svg',body,'顯式求解時間步與結果輸出影格的區別')
    body=text(28,40,'長方形的內部，就是流體所在的位置',23,weight='700')
    body+=rect(140,117,515,140,'#e6f3fa',r=0)+line(140,115,655,115,'#4f745a')+line(140,260,655,260,'#4f745a')
    body+=text(245,96,'Wall（無滑移）',18)+text(245,292,'Wall（無滑移）',18)
    for y in [145,185,225]:body+=arrow(54,y,132,y,'#6b9db8')
    for y in [145,185,225]:body+=arrow(662,y,734,y,'#b78d5c')
    body+=text(32,100,'速度入口',14)+text(669,100,'壓力出口',14)
    body+=text(261,194,'流體域・Planar（平面）',19,weight='700')
    body+=text(80,340,'長度 1 m、間隙 10 mm；不是實心管壁，也不是圓管截面。',15)
    body+=text(28,380,'繪圖縱向放大，未按細長比繪製；不含數值求解資料。',12)
    svg('fluent-channel.svg',body,'二維平行板流體面與入口出口壁面')
    body=text(28,40,'充分發展後，中心速度是平均的 1.5 倍',23,weight='700')
    body+=line(90,95,690,95,'#7c9a80')+line(90,285,690,285,'#7c9a80')+line(100,95,100,285,'#a1b5a7','stroke-dasharray="4 5"')
    pts=[]
    for i in range(101):
        eta=i/100;y=285-190*eta;x=100+490*4*eta*(1-eta);pts.append(f'{x:.2f},{y:.2f}')
    body+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="#609fbd" stroke-width="4"/>'
    for eta in [.15,.3,.5,.7,.85]:
        body+=arrow(100,285-190*eta,100+490*4*eta*(1-eta),285-190*eta,'#92b7c5')
    body+=text(610,198,'umax',20)+text(610,223,'= 1.5 Umean',15)
    body+=text(90,330,'u = 0（壁面）　→　中心最快　→　u = 0（另一壁面）',15)
    body+=text(28,379,'解析形狀示意；入口發展段、圓管與湍流不可直接套用。',12)
    svg('fluent-profile.svg',body,'充分發展平行板層流的拋物線速度剖面')
    body=text(28,40,'三種檢查，一起看才完整',23,weight='700')
    items=[('殘差','方程的數值誤差指標','有下降嗎？有停滯嗎？','#e8f3fa'),('質量守恆','所有邊界的通量收支','進來與出去對得上嗎？','#eff4de'),('關注物理量','壓降、速度剖面等','穩定嗎？細化後仍合理嗎？','#ffeddb')]
    for i,(title,a,b,c) in enumerate(items):
        x=22+260*i;body+=rect(x,88,238,235,c)+text(x+21,136,title,25,weight='700')+text(x+17,187,a,14)+text(x+17,244,b,13)
    body+=text(28,368,'這是檢查面向圖，不是已通過收斂的曲線或門檻。',13)
    svg('fluent-convergence.svg',body,'殘差、質量守恆與物理監測的三向檢查')
    body=text(28,40,'四個模擬入口，從不同問題開始',23,weight='700')
    items=[('Modal','怎麼振？','bend-vs-twist'),('Maxwell','場怎麼分布？','maxwell-potential'),('LS-DYNA','碰撞時發生什麼？','impact-setup'),('Fluent','流體怎麼流？','fluent-channel')]
    for i,(title,sub,_) in enumerate(items):
        x=26+(i%2)*390;y=78+(i//2)*142;body+=rect(x,y,358,121,['#eaf3e0','#fff0d9','#f1e9fa','#e6f3fa'][i])+text(x+20,y+43,title,26,weight='700')+text(x+20,y+84,sub,18)
    body+=text(28,381,'同一套筆記規則：觀念 → 入門案例 → 檢查與排錯',12)
    svg('software-map.svg',body,'模態、電磁場、顯式動力與流體四個專區')
    print('Generated 10 multiphysics SVG teaching diagrams.')
if __name__=='__main__':make()
