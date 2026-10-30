document.querySelectorAll('form[data-preview]').forEach(function(f){
  f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.preview-note');if(n){n.hidden=false;n.scrollIntoView({block:'nearest',behavior:'smooth'});}});
});
document.querySelectorAll('nav.links a').forEach(function(a){a.addEventListener('click',function(){document.getElementById('menu').classList.remove('open');});});
/* Photo grid lightbox: prev/next, Esc, arrow keys, swipe */
(function(){
  var grids=document.querySelectorAll('.pgrid');
  if(!grids.length) return;
  var lb=document.createElement('div');
  lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Photo viewer');
  lb.innerHTML='<figure><img alt=""><figcaption></figcaption></figure><button class="lb-close" aria-label="Close">&times;</button><button class="lb-prev" aria-label="Previous photo">&#8249;</button><button class="lb-next" aria-label="Next photo">&#8250;</button>';
  document.body.appendChild(lb);
  var img=lb.querySelector('img'),cap=lb.querySelector('figcaption'),items=[],i=0,last=null;
  function show(n){
    i=(n+items.length)%items.length;var a=items[i],t=a.querySelector('img');
    img.src=a.href;img.alt=t?t.alt:'';cap.textContent=(t?t.alt.replace(/ \(photo \d+ of \d+\)$/,'')+' — ':'')+(i+1)+' / '+items.length;
    var p=items[(i+1)%items.length];if(p){var pre=new Image();pre.src=p.href;}
  }
  function open(list,n){items=list;last=document.activeElement;lb.hidden=false;document.body.classList.add('lb-open');show(n);lb.querySelector('.lb-close').focus();}
  function close(){lb.hidden=true;img.removeAttribute('src');document.body.classList.remove('lb-open');if(last)last.focus();}
  grids.forEach(function(g){
    var list=Array.prototype.slice.call(g.querySelectorAll('a[data-lb]'));
    list.forEach(function(a,n){a.addEventListener('click',function(e){e.preventDefault();open(list,n);});});
  });
  lb.querySelector('.lb-close').addEventListener('click',close);
  lb.querySelector('.lb-prev').addEventListener('click',function(e){e.stopPropagation();show(i-1);});
  lb.querySelector('.lb-next').addEventListener('click',function(e){e.stopPropagation();show(i+1);});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  document.addEventListener('keydown',function(e){
    if(lb.hidden)return;
    if(e.key==='Escape'){close();}
    else if(e.key==='ArrowLeft'){show(i-1);}
    else if(e.key==='ArrowRight'){show(i+1);}
  });
  var x0=null,y0=null;
  lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
  lb.addEventListener('touchend',function(e){
    if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;
    if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){show(dx<0?i+1:i-1);}
  },{passive:true});
})();
