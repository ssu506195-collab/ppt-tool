(function(){
'use strict';
if(!window.LabMath)return;
var M=window.LabMath;
function element(name,attrs){var n=document.createElementNS('http://www.w3.org/2000/svg',name);Object.keys(attrs||{}).forEach(function(k){n.setAttribute(k,attrs[k]);});return n;}
function add(s,name,attrs,text){var e=element(name,attrs);if(text!==undefined)e.textContent=text;s.appendChild(e);return e;}
function text(s,x,y,t,size,color){return add(s,'text',{x:x,y:y,'font-size':size||16,fill:color||'#365c43','font-family':'Microsoft JhengHei,sans-serif'},t);}
function rect(s,x,y,w,h,c){return add(s,'rect',{x:x,y:y,width:w,height:h,rx:5,fill:c});}
function arrow(s,x,y,dx,dy,color){var a=Math.atan2(dy,dx),ex=x+dx,ey=y+dy;return add(s,'path',{d:'M'+x+' '+y+'L'+ex+' '+ey+'M'+(ex-7*Math.cos(a-.5))+' '+(ey-7*Math.sin(a-.5))+'L'+ex+' '+ey+'L'+(ex-7*Math.cos(a+.5))+' '+(ey-7*Math.sin(a+.5)),fill:'none',stroke:color||'#537f63','stroke-width':2});}
document.querySelectorAll('[data-lab]').forEach(function(root){
 var type=root.dataset.lab,svg=root.querySelector('[data-lab-svg]'),playing=false,raf=0,last=0,elapsed=0,particle=0;
 var controls={};root.querySelectorAll('[data-lab-input]').forEach(function(el){controls[el.dataset.labInput]=el;});
 var play=root.querySelector('[data-lab-play]');
 svg.removeAttribute('hidden');root.querySelector('.lab-fallback').hidden=true;
 function value(k){return Number(controls[k].value);}
 function out(k,t){root.querySelector('[data-lab-output="'+k+'"]').textContent=t;}
 function stat(k,t){root.querySelector('[data-lab-stat="'+k+'"]').textContent=t;}
 function bg(){svg.replaceChildren();rect(svg,0,0,800,340,'#f6f8ee');}
 function render(){
 bg();
 if(type==='electrostatic'){
   var v=value('voltage'),gap=value('gap'),model=M.electric(v,gap),height=80+3*gap,top=175-height/2;
   for(var i=0;i<12;i++){var e=i/11;rect(svg,90,top+i*height/12,500,height/12+1,'rgb('+Math.round(233-100*e)+','+Math.round(160+40*e)+','+Math.round(105+100*e)+')');}
   rect(svg,88,top-13,504,13,'#bc8a61');rect(svg,88,top+height,504,13,'#749cb6');
   for(var x=135;x<560;x+=65)arrow(svg,x,top+13,0,height-26);
   text(svg,610,top+7,v+' V',22);text(svg,610,top+height+12,'0 V',22);
   text(svg,90,32,'顏色：電位 V　箭頭：電場向低電位',16);
   text(svg,160,316,'理想均勻間隙：E = ΔV / d',18);
   out('voltage',v+' V');out('gap',gap+' mm');stat('field',(model.field/1000).toFixed(2));stat('volts',v);stat('distance',gap);
   root.querySelector('[data-lab-insight]').textContent='相同電壓下，間距縮小一半，均勻場強加倍；本圖不模擬尖角與有限電極外部空間。';
 }else if(type==='channel'){
   var u=value('mean'),h=value('gap'),m=M.channel(u,h),pts=[];
   add(svg,'path',{d:'M80 75H650M80 270H650M85 75V270',stroke:'#91ab95','stroke-width':2,fill:'none'});
   for(var i=0;i<=80;i++){var eta=i/80;pts.push((85+470*m.velocity(eta)/m.max)+','+(270-195*eta));}
   add(svg,'polyline',{points:pts.join(' '),stroke:'#6a9fb8','stroke-width':4,fill:'none'});
   for(var j=1;j<8;j++){
      var eta=j/8,y=270-195*eta,len=470*m.velocity(eta)/m.max;arrow(svg,85,y,len,0,'#9dbcc5');
      if(playing){var px=85+((particle*m.velocity(eta)/.045+j*.19)%1)*470;add(svg,'circle',{cx:px,cy:y,r:4,fill:'#c88954'});}
   }
   text(svg,85,42,'充分發展層流：上下壁面 u = 0',18);
   text(svg,570,170,'中心最快',19);text(svg,570,199,'1.5 × Umean',15);
   text(svg,85,307,'剖面水平尺度依 umax 正規化；數值請看下方',15);
   out('mean',u.toFixed(3)+' m/s');out('gap',h+' mm');stat('umax',m.max.toFixed(4));stat('re',m.re.toFixed(1));stat('gradient',m.gradient.toFixed(4));
   root.querySelector('[data-lab-insight]').textContent='平行板層流中心速度為平均的 1.5 倍；相同平均流速下，間隙變小會增加所需壓力梯度。';
 }else{
   var mass=value('mass'),speed=value('speed'),end=M.impact(mass,speed,0).end;
   var t=value('time')/100*end,state=M.impact(mass,speed,t),cx=285+state.x*2200;
   rect(svg,77,100,22,175,'#a9b99f');add(svg,'path',{d:'M100 225H505',stroke:'#b2c3ac','stroke-width':2});
   var springEnd=250;if(state.compression>0)springEnd=cx-35;
   var d='M100 190L112 190';for(var j=0;j<=10;j++)d+='L'+(115+(springEnd-130)*j/10)+' '+(190+(j%2?-11:11));d+='L'+springEnd+' 190';
   add(svg,'path',{d:d,fill:'none',stroke:'#9b8d68','stroke-width':3});
   rect(svg,cx-35,153,70,71,'#9fc4d6');text(svg,cx-26,194,mass.toFixed(1)+' kg',14);
   var sign=state.vx<0?-1:1;arrow(svg,cx,130,sign*50,0,'#b67948');
   text(svg,35,52,'左側彈簧固定；質量朝左接近，回彈後向右',17);
   text(svg,35,300,'t = '+(t*1000).toFixed(2)+' ms　VX = '+state.vx.toFixed(3)+' m/s',17);
   text(svg,35,326,'壓縮量 δ = '+(state.compression*1000).toFixed(2)+' mm（簡化模型）',14);
   text(svg,550,110,'能量比例',17);
   rect(svg,550,145,180*state.kinetic/state.initial,25,'#78a8c1');text(svg,550,136,'動能 K',14);
   rect(svg,550,215,180*state.spring/state.initial,25,'#d69b68');text(svg,550,206,'彈簧能 U',14);
   out('mass',mass.toFixed(1)+' kg');out('speed',speed.toFixed(1)+' m/s');out('time',value('time').toFixed(1)+'%');
   stat('kinetic',state.kinetic.toFixed(4));stat('spring',state.spring.toFixed(4));stat('total',(state.kinetic+state.spring).toFixed(4));
   root.querySelector('[data-lab-insight]').textContent=state.stage+'：本模型 K + U = '+state.initial.toFixed(4)+' J。這個理想能量收支不能直接當作三維方塊的求解結果。';
 }
 }
 function setPlay(on){
   playing=on;if(play){play.textContent=on?'Ⅱ 暫停示意':'▶ 播放示意';play.setAttribute('aria-pressed',String(on));}
   cancelAnimationFrame(raf);last=0;if(on)raf=requestAnimationFrame(tick);
 }
 function tick(now){if(!playing||document.hidden)return;var dt=last?Math.min(now-last,60):0;last=now;
   if(type==='impact'){var q=value('time')+dt/60;if(q>=100){controls.time.value='100';render();setPlay(false);return;}controls.time.value=String(q);}
   else particle+=dt/5000;
   render();raf=requestAnimationFrame(tick);
 }
 Object.keys(controls).forEach(function(key){controls[key].addEventListener('input',function(){if(type==='impact'){setPlay(false);if(key!=='time')controls.time.value='0';}render();});});
 if(play)play.addEventListener('click',function(){if(type==='impact'&&value('time')>=100)controls.time.value='0';setPlay(!playing);render();});
 document.addEventListener('visibilitychange',function(){if(document.hidden)setPlay(false);});
 var reduced=matchMedia('(prefers-reduced-motion: reduce)');if(reduced.addEventListener)reduced.addEventListener('change',function(e){if(e.matches)setPlay(false);});
 window.addEventListener('beforeprint',function(){setPlay(false);render();});
 render();
});
})();
