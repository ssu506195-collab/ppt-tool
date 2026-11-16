const assert=require('node:assert/strict');
const M=require('../assets/lab-math.js');
function near(a,b){assert.ok(Math.abs(a-b)<1e-9*Math.max(1,Math.abs(b)),a+' != '+b)}
near(M.electric(1000,10).field,100000);near(M.electric(1000,5).field,200000);near(M.electric(1000,10).potential(.5),500);
const c=M.channel(.01,10);near(c.max,.015);near(c.velocity(0),0);near(c.velocity(1),0);near(c.velocity(.5),c.max);near(c.gradient,1.2036);near(c.re,998.2*.01*.02/.001003);
let sum=0;for(let i=0;i<10000;i++)sum+=c.velocity((i+.5)/10000)/10000;assert.ok(Math.abs(sum-.01)<1e-9);
near(M.channel(.01,5).gradient,4*c.gradient);
for(const mass of [.5,1,2])for(const speed of [.5,1,2]){
 const a=M.impact(mass,speed,0),tc=a.contactTime,d=a.duration;
 for(let i=0;i<=100;i++){let s=M.impact(mass,speed,a.end*i/100);near(s.kinetic+s.spring,s.initial);assert.ok(s.compression>=0)}
 let peak=M.impact(mass,speed,tc+d/2);near(peak.kinetic,0);near(peak.spring,a.initial);
 near(M.impact(mass,speed,tc).x,0);near(M.impact(mass,speed,tc+d).x,0);near(M.impact(mass,speed,a.end).vx,speed);
}
console.log('PASS: electrostatic field and potential; planar channel no-slip, mean, pressure scaling; impact energy, contact and rebound.');
