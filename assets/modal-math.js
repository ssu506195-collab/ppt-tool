/* Euler–Bernoulli clamped-free bending shapes. Pure geometry, no FEA solver. */
(function(root) {
  'use strict';
  var roots = [1.875104068711961,4.694091132974175,7.854757438237613];
  function raw(n,x) {
    var b=roots[n-1],q=(Math.cosh(b)+Math.cos(b))/(Math.sinh(b)+Math.sin(b));
    return Math.cosh(b*x)-Math.cos(b*x)-q*(Math.sinh(b*x)-Math.sin(b*x));
  }
  function shape(n,x) { return raw(n,x)/Math.abs(raw(n,1)); }
  function nodes(n) {
    var found=[],last=0.001,old=shape(n,last);
    for(var i=2;i<=1000;i++){
      var x=i/1000,y=shape(n,x);
      if(old*y<0){var lo=last,hi=x,sign=old;for(var k=0;k<40;k++){var mid=(lo+hi)/2;if(shape(n,mid)*sign>0)lo=mid;else hi=mid;}found.push((lo+hi)/2);}
      old=y;last=x;
    }
    return found;
  }
  function project(x,y,z) { return [112+520*x+0.74*y,205+0.42*y-z]; }
  function point(kind,x,y,z,phase,amp) {
    var n=kind==='bend2'?2:kind==='bend3'?3:1, a=shape(n,x);
    if(kind==='torsion'){
      var th=0.8*Math.sin(Math.PI*x/2)*phase*amp,cy=y*Math.cos(th)-z*Math.sin(th),cz=y*Math.sin(th)+z*Math.cos(th);
      return project(x,cy,cz);
    }
    if(kind==='side') y+=80*a*phase*amp;
    else z+=65*a*phase*amp;
    return project(x,y,z);
  }
  var api={roots:roots,raw:raw,shape:shape,nodes:nodes,point:point,project:project};
  root.ModalMath=api;
  if(typeof module!=='undefined' && module.exports)module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
