"""Reusable analytic teaching widgets for Maxwell, LS-DYNA and Fluent."""
def render_lab(name,prefix=''):
    definitions={
      'electrostatic':('電壓與間距，怎麼改變電場？','maxwell-potential','理想平行板解析式；介質均勻、無空間電荷，不含邊緣效應。色帶依當次電位差正規化，箭頭代表方向，線數與箭頭長度不是場強。','maxwell-basics',[
        ('voltage','上板電壓',100,2000,100,1000,'V'),('gap','板間距',5,30,1,10,'mm')],[('field','場強','kV/m'),('volts','電位差','V'),('distance','間距','mm')]),
      'impact':('碰撞時，能量跑去哪裡？','impact-energy','無阻尼、無摩擦的單自由度質量＋壓縮彈簧解析模型。k = 10000 N/m、接觸前間隙 20 mm；與三維方塊案例的材料和尺寸分開。播放經慢放，不是 LS-DYNA 結果。','lsdyna-basics',[
        ('mass','質量',.5,2,.1,1,'kg'),('speed','起始速率',.5,2,.1,1,'m/s'),('time','時間進度',0,100,.2,0,'%')],[('kinetic','動能 K','J'),('spring','彈簧能 U','J'),('total','K + U','J')]),
      'channel':('流速與間距，怎麼改變剖面？','fluent-profile','均勻牛頓流體、充分發展平行板層流解析式。ρ = 998.2 kg/m³、μ = 0.001003 Pa·s、Dh = 2H；不含入口發展段。粒子用示意慢放，不是 Fluent 求解動畫。','fluent-basics',[
        ('mean','平均流速',.005,.03,.001,.01,'m/s'),('gap','全間隙',5,20,1,10,'mm')],[('umax','中心速度','m/s'),('re','Re（Dh）',''),('gradient','壓降／長度','Pa/m')])
    }
    title,image,note,source,controls,metrics=definitions[name]
    fields=''.join(f'<label>{label}<input type="range" data-lab-input="{key}" min="{lo}" max="{hi}" step="{step}" value="{value}" aria-label="{label}"><output data-lab-output="{key}">{value} {unit}</output></label>' for key,label,lo,hi,step,value,unit in controls)
    values=''.join(f'<div><span>{label}</span><b data-lab-stat="{key}">—</b><small>{unit}</small></div>' for key,label,unit in metrics)
    play='<button type="button" class="play-button" data-lab-play aria-pressed="false">▶ 播放示意</button>' if name!='electrostatic' else ''
    return f'''<div class="mode-explorer lab-explorer" data-lab="{name}"><div class="explorer-heading"><div><span class="eyebrow">先玩再懂 / ANALYTIC PLAYGROUND</span><h3>{title}</h3></div><span class="sticker">解析／概念</span></div><div class="mode-stage lab-stage"><img class="lab-fallback" src="{prefix}assets/diagrams/{image}.svg" alt="{title}的靜態教學示意"><svg viewBox="0 0 800 340" data-lab-svg role="img" aria-label="{title}" hidden></svg></div><div class="lab-stats">{values}</div><div class="mode-controls lab-controls">{play}{fields}</div><p class="lab-insight" data-lab-insight></p><p class="diagram-note">{note} <a href="{prefix}articles/{source}.html#sources">查看依據 ↗</a></p></div>'''
