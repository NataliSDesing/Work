  /* ===== станки: рисуются из параметров (линейный изометрический стиль) ===== */
  var MM={
    'ByStar Fiber 3015':['Bystronic','3000×1500',300,150,'A','bevel','swing',2],
    'ByStar Fiber 4020':['Bystronic','4000×2000',360,180,'A','bevel','swing',3],
    'BySprint Fiber 3015':['Bystronic','3000×1500',300,150,'B','bevel','swing',2],
    'TruLaser 3030':['Trumpf','3000×1500',300,150,'B','slant','stand',2],
    'TruLaser 5030':['Trumpf','3000×1500',300,150,'A','slant','stand',2],
    'TruLaser 3060':['Trumpf','6000×2000',440,160,'A','slant','stand',3],
    'Bodor i5 3015':['Bodor','3000×1500',300,150,'B','flat','stand',2],
    'Bodor P 3015':['Bodor','3000×1500',300,150,'C','flat','stand',2],
    'Bodor C 3015':['Bodor','3000×1500',300,150,'C','flat','stand',1],
    'GWEIKE LF3015':['HSG Laser','3000×1500',300,150,'C','flat','swing',2],
    'GWEIKE LF4020':['HSG Laser','4000×2000',360,180,'C','flat','swing',3],
    'GWEIKE LF6025':['HSG Laser','6000×2500',440,190,'C','flat','swing',3],
    'G3015':["Han's Laser",'3000×1500',300,150,'C','barrel','tall',2],
    'G4020':["Han's Laser",'4000×2000',360,180,'C','barrel','tall',3],
    'G6025':["Han's Laser",'6000×2500',440,190,'C','barrel','tall',3]};
  function machineSVG(brand,L,W,kind,roof,pult,doors){
    var D=!!document.querySelector('.ll-d'),C=Math.cos(Math.PI/6),NAVY=D?'#EFEFEF':'#072730',PAPER=D?'#0A2A34':'#F8F9F9',BLUE='#5EA7BB',LIME='#E8FC5C',GREY=D?'#9FB6BE':'#798591',ORANGE='#FF860D',LOW=D?'#134556':'#E3EFF3';
    var bb={a:1e9,b:1e9,c:-1e9,d:-1e9};
    function P(x,y,z){var X=(x-y)*C,Y=(x+y)*.5-z;if(X<bb.a)bb.a=X;if(Y<bb.b)bb.b=Y;if(X>bb.c)bb.c=X;if(Y>bb.d)bb.d=Y;return[X,Y]}
    function r(n){return Math.round(n*10)/10}
    function pt(q){var p=P(q[0],q[1],q[2]);return r(p[0])+','+r(p[1])}
    function dd(pts,close){return'M'+pts.map(function(q){var p=P(q[0],q[1],q[2]);return r(p[0])+' '+r(p[1])}).join(' L')+(close?' Z':'')}
    function Layer(sw){this.i=[];this.sw=sw||1.3}
    Layer.prototype.box=function(x0,y0,z0,x1,y1,z1,o){o=o||{};var st=o.stroke||NAVY,fl=o.fill||PAPER,sw=o.sw||this.sw,g='';
      function poly(p){return'<polygon points="'+p.map(pt).join(' ')+'" fill="'+fl+'" stroke="'+st+'" stroke-width="'+sw+'"/>'}
      function ln(a,b){var A=P(a[0],a[1],a[2]),B=P(b[0],b[1],b[2]);return'<line x1="'+r(A[0])+'" y1="'+r(A[1])+'" x2="'+r(B[0])+'" y2="'+r(B[1])+'" stroke="'+st+'" stroke-width="'+r(sw*.6)+'"/>'}
      g+=poly([[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])+poly([[x1,y0,z0],[x1,y1,z0],[x1,y1,z1],[x1,y0,z1]])+poly([[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]]);
      for(var i=1;i<(o.n||0);i++){
        if(o.pleat==='x'){var x=x0+(x1-x0)*i/o.n;g+=ln([x,y0,z1],[x,y1,z1])+ln([x,y1,z0],[x,y1,z1])}
        if(o.pleat==='y'){var y=y0+(y1-y0)*i/o.n;g+=ln([x0,y,z1],[x1,y,z1])+ln([x1,y,z0],[x1,y,z1])}}
      this.i.push([(x0+x1)/2+(y0+y1)/2+(z0+z1)/2,g])};
    Layer.prototype.line=function(pts,stroke,sw,depth,o){o=o||{};
      this.i.push([depth||0,'<path d="'+dd(pts,o.close)+'" fill="none" stroke="'+stroke+'" stroke-width="'+sw+'"'+(o.dash?' stroke-dasharray="'+o.dash+'"':'')+(o.cls?' class="'+o.cls+'" pathLength="1"':'')+'/>'])};
    Layer.prototype.quad=function(pts,fill,op){this.i.push([1e5,'<path d="'+dd(pts,true)+'" fill="'+fill+'" fill-opacity="'+(op||1)+'" stroke="'+NAVY+'" stroke-width=".9"/>'])};
    Layer.prototype.svg=function(){return this.i.sort(function(a,b){return a[0]-b[0]}).map(function(t){return t[1]}).join('')};
    var GX0=Math.floor(L*.38),GX1=GX0+26,tx0=-Math.floor(L*.30),tx1=Math.floor(L*.40),hx0=-52,hx1=52;
    var X0=-14,X1=L+14,Y0=-40,Y1=W+40,Z=122,z0=34,z1=Z;
    var ACC={'Bystronic':LIME,'Trumpf':BLUE,'Bodor':ORANGE,'HSG Laser':NAVY,"Han's Laser":GREY}[brand]||LIME;
    var base=new Layer(),sheet=new Layer(1.1),cabB=new Layer(1),gan=new Layer(),head=new Layer(),cabF=new Layer(1),ex=new Layer();
    function post(x,y){return[[x,y,z0],[x,y,z1]]}
    base.box(0,0,0,L,W,34);base.box(8,8,34,L-8,W-8,38);base.box(14,14,38,L-14,W-14,41);base.box(0,-14,34,L,0,44);base.box(0,W,34,L,W+14,44);
    var nb=Math.max(7,Math.floor(L/33)),half=L/2,lo={stroke:BLUE,fill:LOW,pleat:'x',n:Math.floor(nb/2)+1};
    [[2,half-2],[half+2,L-2]].forEach(function(s){base.box(s[0],-14,44,s[1],0,60,lo);base.box(s[0],W,44,s[1],W+14,60,lo)});
    sheet.box(18,18,41,L-18,W-18,46,{stroke:GREY,sw:1.1});
    var cx0=L*.22,cy0=W*.24,cx1=L*.62,cy1=W*.72;
    sheet.line([[cx0,cy0,46],[cx1,cy0,46],[cx1,cy1,46],[cx0+40,cy1,46],[cx0,cy1-30,46]],ORANGE,1.6,1e6,{close:1,cls:'cut'});
    sheet.line([[cx1+30,W*.5,46],[cx1+60,W*.5+10,46],[cx1+60,W*.5-10,46]],ORANGE,1.6,1e6,{close:1,cls:'cut2'});
    cabB.line(post(X0,Y0),GREY,1);cabB.line(post(X1,Y0),GREY,1);cabB.line(post(X0,Y1),GREY,1);
    cabB.line([[X0,Y0,z1],[X1,Y0,z1]],GREY,1);cabB.line([[X0,Y0,z1],[X0,Y1,z1]],GREY,1);
    gan.box(GX0-2,-24,34,GX1+2,-2,66);gan.box(GX0-2,W+2,34,GX1+2,W+26,66);gan.box(GX0,-24,66,GX1,W+26,96);
    var up={stroke:NAVY,fill:LIME,pleat:'y',n:8};
    gan.box(GX1,-20,70,GX1+14,W*.4,92,up);gan.box(GX1,W*.6,70,GX1+14,W+22,92,up);
    var hy0=W*.5-16;
    head.box(GX1,hy0,66,GX1+22,hy0+32,100);head.box(GX1+6,hy0+10,44,GX1+16,hy0+22,66);
    head.line([[GX1+11,hy0+16,44],[GX1+11,hy0+16,36]],ORANGE,1.8,1e6,{cls:'m-beam'});
    cabF.line([[X1,Y0,z0],[X1,Y1,z0],[X0,Y1,z0]],GREY,1);cabF.line(post(X1,Y1),GREY,1.2);cabF.line(post(X1,Y0),GREY,1.2);cabF.line(post(X0,Y1),GREY,1.2);
    var rf=[[X0,Y0,z1],[X1,Y0,z1],[X1,Y1,z1],[X0,Y1,z1]],mid=(Y0+Y1)/2;
    if(roof==='slant'){
      cabF.line([[X0,Y0,z1],[X1,Y0,z1],[X1,Y1,z1-38],[X0,Y1,z1-38]],NAVY,1.3,5,{close:1});cabF.line([[X1,Y0,z1],[X1,Y1,z1-38]],NAVY,1.3,5);cabF.line([[X1,Y1,z1-38],[X1,Y1,z1-56]],GREY,1)}
    else if(roof==='bevel'){
      cabF.line(rf,NAVY,1.3,5,{close:1});cabF.line([[X0,Y1-22,z1],[X1,Y1-22,z1]],NAVY,1.1,5);cabF.line([[X0,Y1,z1-22],[X1,Y1,z1-22]],NAVY,1.1,5);cabF.line([[X1,Y1-22,z1],[X1,Y1,z1-22]],NAVY,1.1,5)}
    else if(roof==='barrel'){
      cabF.line(rf,NAVY,1.3,5,{close:1});cabF.line([[X1,Y0,z1],[X1,mid,z1+20],[X1,Y1,z1]],NAVY,1.3,5);cabF.line([[X0,mid,z1+20],[X1,mid,z1+20]],NAVY,1.1,5);cabF.line([[X0,Y0,z1],[X0,mid,z1+20],[X0,Y1,z1]],GREY,1,5)}
    else cabF.line(rf,NAVY,1.3,5,{close:1});
    var zt=z1-(roof==='slant'?38:0),dw=(X1-X0)/(doors+1);
    for(var i=1;i<=doors;i++){var x=X0+dw*i;cabF.line([[x,Y1,z0],[x,Y1,zt]],GREY,1,0,{dash:'3 3'})}
    cabF.line([[X0+14,Y1,z0+24],[X0+44,Y1,zt-10]],BLUE,1);cabF.line([[X0+28,Y1,z0+24],[X0+58,Y1,zt-10]],BLUE,1);
    cabF.quad([[X0,Y1,z0+2],[X1,Y1,z0+2],[X1,Y1,z0+14],[X0,Y1,z0+14]],ACC);
    if(brand==='HSG Laser')cabF.quad([[X0,Y1,zt-28],[X1,Y1,zt-28],[X1,Y1,zt],[X0,Y1,zt]],NAVY,.85);
    if(brand==="Han's Laser")cabF.quad([[X0,Y1,zt-28],[X1,Y1,zt-28],[X1,Y1,zt],[X0,Y1,zt]],GREY,.35);
    if(kind!=='B'&&brand!=='Trumpf'){var e=Math.floor(L*(kind==='A'?.46:.38));
      ex.box(X1+4,10,18,X1+4+e,W-10,30);ex.box(X1+10,18,30,X1+4+e-6,W-18,36,{stroke:GREY,sw:1.1});ex.box(X1+4,8,0,X1+12,16,18);ex.box(X1+4+e-8,W-16,0,X1+4+e,W-8,18)}
    if(brand==='Trumpf'&&kind!=='B'){var ey=Math.floor(W*.55);ex.box(30,Y1+4,18,L-30,Y1+4+ey,30);ex.box(38,Y1+10,30,L-38,Y1+4+ey-6,36,{stroke:GREY,sw:1.1})}
    if(brand==='Bodor'){ex.box(X0-60,Y0+8,34,X0-4,Y0+92,150);for(var k=1;k<4;k++)ex.box(X0-56,Y0+91,34+k*26,X0-8,Y0+93,36+k*26,{stroke:GREY,sw:.8})}
    if(brand==='Bystronic'&&kind!=='B')ex.box(X1-6,Y0-20,0,X1+30,Y0+4,70);
    var px,py;
    if(pult==='swing'){px=X1-10;py=Y1+22;ex.box(px-12,py,0,px,py+12,78);ex.box(px-40,py-6,78,px,py+22,100)}
    else if(pult==='tall'){px=X0+40;py=Y1+24;ex.box(px,py,0,px+16,py+16,100);ex.box(px-14,py-4,100,px+30,py+22,126)}
    else{px=X0+70;py=Y1+26;ex.box(px,py,0,px+30,py+24,70);ex.box(px+4,py+2,70,px+26,py+22,94)}
    ex.box(X0+10,Y0+10,Z,X0+22,Y0+22,Z+12,{fill:ACC});
    function o2(dx,dy){return r((dx-dy)*C)+'px,'+r((dx+dy)*.5)+'px'}
    var body='<g>'+base.svg()+'</g><g>'+sheet.svg()+'</g><g>'+cabB.svg()+'</g>'+
      '<g class="m-gantry" style="--gx0:'+o2(tx0,0)+';--gx1:'+o2(tx1,0)+'">'+gan.svg()+'<g class="m-head" style="--hy0:'+o2(0,hx0)+';--hy1:'+o2(0,hx1)+'">'+head.svg()+'</g></g>'+
      '<g>'+cabF.svg()+'</g><g>'+ex.svg()+'</g>';
    var a=bb.a-20,b=bb.b-30;
    return'<svg class="mach" viewBox="'+r(a)+' '+r(b)+' '+r(bb.c-a+20)+' '+r(bb.d-b+20)+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Схема станка">'+body+'</svg>'}
  function drawMachine(){
    var box=$('#llMachine'),cap=$('#llMachCap'),m=MM[st.model];if(!box||!m)return;
    box.innerHTML=machineSVG(m[0],m[2],m[3],m[4],m[5],m[6],m[7]);
    if(cap)cap.textContent=(st.model.toLowerCase().indexOf(st.brand.split(' ')[0].toLowerCase())===0?st.model:st.brand+' '+st.model)+' · рабочее поле '+m[1]+' мм'}
