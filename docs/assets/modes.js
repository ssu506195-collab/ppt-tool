(function(){
  'use strict';
  if(!window.ModalMath)return;
  var M=window.ModalMath;
  var labels={
    bend1:['一階彎曲 · Z 向','整支樑往同一方向彎。除了固定端，沒有其他內部節點。'],
    side:['一階側向彎曲 · Y 向','換到另一個方向彎，形狀仍屬一階彎曲家族。三維模型會同時出現不同方向的模態。'],
    bend2:['二階彎曲 · Z 向','中間會出現一個內部節點（約 x/L = 0.783），節點兩側在同一瞬間往相反方向移動。'],
    bend3:['三階彎曲 · Z 向','有兩個內部節點（約 x/L = 0.504、0.868），形成三段交替彎動的區域。'],
    torsion:['扭轉 · 概念示意','截面繞長軸旋轉，和中心線彎曲不同。此圖使用幾何插值，不含截面翹曲，也不是扭轉求解。']
  };
  function elem(name,attrs){var e=document.createElementNS('http://www.w3.org/2000/svg',name);Object.keys(attrs||{}).forEach(function(k){e.setAttribute(k,attrs[k]);});return e;}
  function put(parent,name,attrs,text){var e=elem(name,attrs);if(text)e.textContent=text;parent.appendChild(e);return e;}
  document.querySelectorAll('[data-mode-explorer]').forEach(function(root,index){
    var svg=root.querySelector('[data-mode-svg]'),fallback=root.querySelector('.mode-fallback');
    var kind='bend1',phase=90,amp=1,playing=false,raf=0,last=0,visible=true;
    var play=root.querySelector('[data-mode-play]'),phaseInput=root.querySelector('[data-mode-phase]'),ampInput=root.querySelector('[data-mode-amplitude]');
    var uid='mode-'+index+'-';
    svg.hidden=false;svg.removeAttribute('hidden');fallback.hidden=true;
    var defs=put(svg,'defs');
    var pattern=put(defs,'pattern',{id:uid+'hatch',width:7,height:7,patternUnits:'userSpaceOnUse',patternTransform:'rotate(35)'});
    put(pattern,'path',{d:'M0 0V7',stroke:'#8ba491','stroke-width':2});
    put(svg,'rect',{x:0,y:0,width:800,height:340,rx:18,fill:'#f6f8ee'});
    put(svg,'rect',{x:75,y:151,width:22,height:103,fill:'url(#'+uid+'hatch)',stroke:'#6f8f78'});
    put(svg,'path',{d:'M100 205H677',stroke:'#98ad9d','stroke-width':1.5,'stroke-dasharray':'6 6'});
    put(svg,'text',{x:35,y:285,fill:'#607c6c','font-size':14},'固定端');
    put(svg,'text',{x:626,y:285,fill:'#607c6c','font-size':14},'自由端');
    var axis=put(svg,'g',{transform:'translate(707 93)'});
    put(axis,'path',{d:'M0 20H38M0 20V-10M0 20L19 34',fill:'none',stroke:'#708f7c','stroke-width':1.5});
    put(axis,'text',{x:43,y:25,'font-size':12,fill:'#708f7c'},'X');
    put(axis,'text',{x:-6,y:-16,'font-size':12,fill:'#708f7c'},'Z');
    put(axis,'text',{x:23,y:43,'font-size':12,fill:'#708f7c'},'Y');
    var ribbons=put(svg,'g'),nodeGroup=put(svg,'g'),polys=[];
    for(var i=0;i<44;i++){
      polys.push([put(ribbons,'polygon',{'stroke-width':0.7,stroke:'#526f5a'}),put(ribbons,'polygon',{'stroke-width':0.7,stroke:'#526f5a'})]);
    }
    function shapeNumber(){return kind==='bend2'?2:kind==='bend3'?3:1;}
    function polygon(points){return points.map(function(p){return p[0].toFixed(2)+','+p[1].toFixed(2);}).join(' ');}
    function updateNodes(){
      nodeGroup.replaceChildren();
      if(kind!=='bend2'&&kind!=='bend3')return;
      M.nodes(shapeNumber()).forEach(function(x){
        var p=M.project(x,0,0);
        put(nodeGroup,'circle',{cx:p[0],cy:p[1],r:5,fill:'#c16e5e',stroke:'#fff','stroke-width':2});
        put(nodeGroup,'path',{d:'M'+p[0]+' '+(p[1]+8)+'v35',stroke:'#bd7b68','stroke-dasharray':'3 4'});
        put(nodeGroup,'text',{x:p[0],y:p[1]+61,'text-anchor':'middle','font-size':12,fill:'#9f5c4a'},'x/L ≈ '+x.toFixed(3));
      });
    }
    function render(){
      var v=Math.sin(phase*Math.PI/180),n=shapeNumber(),maxMove=kind==='torsion'?2*Math.hypot(18,5)*Math.sin(0.8*amp/2):kind==='side'?80*amp:65*amp;
      for(var i=0;i<44;i++){
        var a=i/44,b=(i+1)/44;
        function p(x,y,z){return M.point(kind,x,y,z,v,amp);}
        var top=[p(a,-18,5),p(b,-18,5),p(b,18,5),p(a,18,5)],side=[p(a,18,5),p(b,18,5),p(b,18,-5),p(a,18,-5)];
        var m=kind==='torsion'?2*Math.hypot(18,5)*Math.abs(Math.sin(0.8*Math.sin(Math.PI*(a+b)/4)*v*amp/2))/maxMove:Math.abs(M.shape(n,(a+b)/2)*v);
        m=Math.min(1,m);
        var c=[129,191,225].map(function(x,j){return Math.round(x+([237,156,105][j]-x)*m);});
        polys[i][0].setAttribute('points',polygon(side));polys[i][0].setAttribute('fill','#b5c9ac');
        polys[i][1].setAttribute('points',polygon(top));polys[i][1].setAttribute('fill','rgb('+c.join(',')+')');
      }
      phaseInput.value=String(Math.round(phase));root.querySelector('[data-phase-output]').textContent=Math.round(phase)+'°';
      root.querySelector('[data-amplitude-output]').textContent=amp.toFixed(1)+'×';
    }
    function setPlaying(value){
      playing=value;play.textContent=value?'Ⅱ 暫停':'▶ 播放';play.setAttribute('aria-pressed',String(value));
      cancelAnimationFrame(raf);last=0;if(value&&!document.hidden&&visible)raf=requestAnimationFrame(tick);
    }
    function tick(time){
      if(!playing||document.hidden||!visible)return;
      if(last)phase=(phase+Math.min(time-last,50)*0.07)%360;
      last=time;render();raf=requestAnimationFrame(tick);
    }
    root.querySelectorAll('[data-mode]').forEach(function(button){button.addEventListener('click',function(){
      kind=button.dataset.mode;phase=90;setPlaying(false);
      root.querySelectorAll('[data-mode]').forEach(function(b){var active=b===button;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
      root.querySelector('[data-mode-name]').textContent=labels[kind][0];root.querySelector('[data-mode-description]').textContent=labels[kind][1];
      svg.setAttribute('aria-label',labels[kind][0]+'教學示意');updateNodes();render();
    });});
    play.addEventListener('click',function(){setPlaying(!playing);});
    phaseInput.addEventListener('input',function(){setPlaying(false);phase=Number(phaseInput.value);render();});
    ampInput.addEventListener('input',function(){amp=Number(ampInput.value);render();});
    document.addEventListener('visibilitychange',function(){if(document.hidden){cancelAnimationFrame(raf);last=0;}else if(playing&&visible){raf=requestAnimationFrame(tick);}});
    if('IntersectionObserver'in window)new IntersectionObserver(function(entries){var was=visible;visible=entries[0].isIntersecting;if(!visible){cancelAnimationFrame(raf);last=0;}else if(!was&&playing&&!document.hidden){raf=requestAnimationFrame(tick);}}).observe(root);
    var reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    if(reduced.addEventListener)reduced.addEventListener('change',function(event){if(event.matches)setPlaying(false);});
    window.addEventListener('beforeprint',function(){setPlaying(false);phase=90;render();});
    updateNodes();render();
  });
})();
