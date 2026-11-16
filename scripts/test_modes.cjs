const assert=require('node:assert/strict');
const M=require('../assets/modal-math.js');
for(let n=1;n<=3;n++){
 const b=M.roots[n-1],q=(Math.cosh(b)+Math.cos(b))/(Math.sinh(b)+Math.sin(b)),norm=Math.abs(M.raw(n,1));
 assert.ok(Math.abs(Math.cosh(b)*Math.cos(b)+1)<1e-9,'Characteristic root');
 assert.ok(Math.abs(M.shape(n,0))<1e-12,'Clamped displacement');
 assert.ok(Math.abs((M.shape(n,1e-5)-M.shape(n,-1e-5))/2e-5)<1e-6,'Clamped slope');
 const moment=b*b*(Math.cosh(b)+Math.cos(b)-q*(Math.sinh(b)+Math.sin(b)))/norm;
 const shear=b*b*b*(Math.sinh(b)-Math.sin(b)-q*(Math.cosh(b)+Math.cos(b)))/norm;
 assert.ok(Math.abs(moment)<1e-7,'Free-end moment');
 assert.ok(Math.abs(shear)<1e-7,'Free-end shear');
 assert.ok(Math.abs(Math.abs(M.shape(n,1))-1)<1e-12,'Normalized free end');
 assert.equal(M.nodes(n).length,n-1,'Internal node count');
}
assert.ok(Math.abs(M.nodes(2)[0]-0.7834)<0.0001);
assert.ok(Math.abs(M.nodes(3)[0]-0.5035)<0.0001);
assert.ok(Math.abs(M.nodes(3)[1]-0.8677)<0.0001);
for(const kind of ['bend1','side','bend2','bend3','torsion'])for(const phase of [-1,0,1]){
 assert.deepEqual(M.point(kind,0,18,5,phase,1),M.project(0,18,5),'Entire fixed section stays still');
 for(const p of M.point(kind,0.5,18,5,phase,1))assert.ok(Number.isFinite(p));
}
assert.notDeepEqual(M.point('side',1,0,0,1,1),M.point('bend1',1,0,0,1,1),'Different bending directions');
console.log('PASS: 3 characteristic roots, clamped/free boundary conditions, 0/1/2 internal nodes, 5 fixed-end geometries and direction distinction.');
