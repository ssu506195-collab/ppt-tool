(function(root){
'use strict';
function electric(volts,gapMM){var d=gapMM/1000;return {field:Math.abs(volts)/d,gap:d,potential:function(eta){return volts*eta;}};}
function channel(mean,gapMM){var h=gapMM/1000,rho=998.2,mu=.001003;return{height:h,mean:mean,max:1.5*mean,re:rho*mean*2*h/mu,gradient:12*mu*mean/(h*h),massPerWidth:rho*mean*h,velocity:function(eta){return 6*mean*eta*(1-eta);}};}
function impact(m,v,time){var k=10000,gap=.02,w=Math.sqrt(k/m),tc=gap/v,duration=Math.PI/w,end=2*tc+duration,dx=0,x=gap-v*time,vx=-v,stage='接觸前';
if(time>=tc&&time<=tc+duration){var q=w*(time-tc);dx=v/w*Math.sin(q);x=-dx;vx=-v*Math.cos(q);stage=q<Math.PI/2?'壓縮中':'回彈中';}
else if(time>tc+duration){x=v*(time-tc-duration);vx=v;stage='已分離';}
return{x:x,vx:vx,compression:Math.max(0,dx),kinetic:.5*m*vx*vx,spring:.5*k*dx*dx,initial:.5*m*v*v,contactTime:tc,duration:duration,end:end,stage:stage};}
var api={electric:electric,channel:channel,impact:impact};root.LabMath=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
