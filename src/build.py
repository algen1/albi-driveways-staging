"""Build the Albi Driveways STAGING static site into ../dist.

Usage:  python3 src/build.py      (from the repo root, or any directory)
Inputs: src/data/media.json (Media Manager file list), src/data/photogrid.json
        (photo grids per category), templates/assets/ (CSS + JS, copied as is).
Output: dist/ (wiped and regenerated) and src/data/placeholders.json.
"""
import json, os, re, html, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,'src','data')
OUT=os.path.join(ROOT,'dist')
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(os.path.join(ROOT,'templates','assets'),os.path.join(OUT,'assets'))
M=json.load(open(os.path.join(DATA,'media.json')))['files']
def U(i,w=1200,h=900):
    if isinstance(i,str): u=i
    else: u=M[i][1]
    base=u.rsplit('/',1)[1]; name=base.split('~')[0]
    return f"{u}/v1/fill/w_{w},h_{h},al_c,q_80,enc_auto/{name}.jpg"
LOGO="https://static.wixstatic.com/media/cc9fca_2d8154d6e9ce49b5be7a1d594bad4ba4~mv2.png"
BA=[("https://static.wixstatic.com/media/cc9fca_b73773f62448434d98a93dc7378d1e43~mv2.jpg","https://static.wixstatic.com/media/cc9fca_804b3ee4a53b4376aa30ee4c80334b1e~mv2.jpg","Side passage paving"),
    ("https://static.wixstatic.com/media/cc9fca_ebe642d064974da080ade05e24732ca5~mv2_d_1600_1200_s_2.jpg","https://static.wixstatic.com/media/cc9fca_ba470975633f4bcca64448eb3db14037~mv2_d_1600_1200_s_2.jpg","Garden clearance to new lawn"),
    (274,205,"Front garden to herringbone block-paving driveway")]
TEL='tel:+447909600964'; WA='https://wa.me/447909600964'; MAIL='mailto:albidriveways@gmail.com'
GBP='https://www.google.com/maps/place/Albi+Driveways+-+Patio,+Fencing+%26+Turfing/data=!4m2!3m1!1s0x48766d16af9b7369:0x182d48ddaf469a42'
AREAS=["Ruislip","Eastcote","Ickenham","Northwood","Pinner","Harrow","Wembley","Hillingdon","Uxbridge","Watford","Mill Hill"]
def P(t): return f'<mark class="ph">[PLACEHOLDER: {html.escape(t)}]</mark>'
PH=set()
def ph(t): PH.add(t); return P(t)

GAL={
 'drive':[118,78,9,103,139,212,124,70,92,82,163,205,84,162,117,128],
 'patio':[35,3,37,44,46,53,61,63,195,196,55,60],
 'fence':[27,24,25,28,29,30,32,34,197,200,26,31],
 'turf':[15,14,50,51,146,154,189,190,85,42],
 'brick':[47,68,91,147,175,177,178,186,191],
}
ALT={'drive':'Block-paving driveway laid by Albi Driveways','patio':'Garden patio laid by Albi Driveways','fence':'New garden fencing installed by Albi Driveways','turf':'Freshly laid turf lawn in a back garden','brick':'Brick steps and edging by Albi Driveways'}

NAV=[('Home',''),('Driveways','driveways/'),('Patios','patios/'),('Fencing','fencing/'),('Turfing & Garden','turfing-garden/'),('Our Work','before-afters/'),('Areas','areas-we-cover/'),('Reviews','reviews/')]

def page(slug,title,desc,body,schema=None,active=''):
    pre='' if slug=='' else '../'
    L=lambda p: pre+p if p else (pre or './')
    nav=''.join(f'<a href="{L(p)}"{" class=on" if p==active else ""}>{html.escape(n)}</a>' for n,p in NAV)
    sch=''.join(f'<script type="application/ld+json">{json.dumps(s,ensure_ascii=False)}</script>' for s in (schema or []))
    b=body.replace('{{R}}',pre if pre else '')
    doc=f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/site.css">{sch}
</head><body>
<div class="ribbon" role="note">STAGING PREVIEW – not the live site</div>
<div class="topbar"><div class="wrap"><span><span class="stars">★★★★★</span> <b>5.0 on Google</b> · {P('confirm review count – 160')}</span><span class="hide-m">Family-run · {P('confirm 27+ years')} · Free, no-obligation quotes</span><a href="{TEL}"><b>07909 600964</b></a></div></div>
<header class="nav"><div class="wrap">
<a class="brand" href="{L('')}"><img src="{LOGO}" alt="Albi Driveways logo"><span>ALBI <em>DRIVEWAYS</em></span></a>
<nav class="links" id="menu">{nav}</nav>
<div class="nav-cta"><a class="tel" href="{TEL}">📞 07909 600964</a><a class="btn btn-red" href="{L('contact/')}">Free quote</a><button class="burger" aria-label="Menu" onclick="document.getElementById('menu').classList.toggle('open')">☰</button></div>
</div></header>
<main>{b}</main>
<div class="band"><div class="wrap">
  <div><h2>Ready for a free, no-obligation quote?</h2><p>Driveways, patios, fencing and turfing across Ruislip, North West London and Watford.</p></div>
  <div class="ctas"><a class="btn btn-dark" href="{L('contact/')}">Get a free quote</a><a class="btn btn-ghost" href="{TEL}">📞 07909 600964</a><a class="btn btn-wa" href="{WA}">💬 WhatsApp</a></div>
</div></div>
<footer><div class="wrap"><div class="cols">
<div><div class="brand"><img src="{LOGO}" alt=""><span style="color:#fff">ALBI <em>DRIVEWAYS</em></span></div><p style="margin-top:12px">Family-run block-paving driveways, patios, fencing and turfing, based in Ruislip (HA4).</p></div>
<div><h4>Services</h4><a href="{L('driveways/')}">Driveways</a><a href="{L('patios/')}">Patios</a><a href="{L('fencing/')}">Fencing</a><a href="{L('turfing-garden/')}">Turfing &amp; garden work</a><a href="{L('brickwork/')}">Brickwork (unconfirmed)</a></div>
<div><h4>Local pages</h4><a href="{L('driveways-ruislip/')}">Driveways Ruislip</a><a href="{L('driveways-eastcote/')}">Driveways Eastcote</a><a href="{L('driveways-pinner/')}">Driveways Pinner</a><a href="{L('fencing-ruislip/')}">Fencing Ruislip</a><a href="{L('fencing-northwood/')}">Fencing Northwood</a><a href="{L('areas-we-cover/')}">All areas</a></div>
<div><h4>Contact</h4><a href="{TEL}">07909 600964</a><a href="{WA}">WhatsApp</a><a href="{MAIL}">albidriveways@gmail.com</a><a href="{L('contact/')}">Free quote form</a><a href="https://www.instagram.com/albidriveways/">Instagram</a><a href="https://www.facebook.com/albidriveway">Facebook</a><a href="{GBP}">Google reviews</a></div>
</div><div class="copy">© 2026 Albi Driveways · STAGING PREVIEW for owner review – not the live site, not indexed. Yellow [PLACEHOLDER] tags mark details still to be confirmed.</div></div></footer>
<div class="mbar"><a href="{TEL}" style="background:#161616">📞 Call</a><a href="{WA}" style="background:#1fa855">💬 WhatsApp</a><a href="{L('contact/')}" style="background:#d71920">Free quote</a></div>
<script src="{pre}assets/site.js"></script>
</body></html>'''
    d=os.path.join(OUT,slug); os.makedirs(d,exist_ok=True)
    doc=re.sub(r'href="((?:\.\./)?(?:[a-z-]+/)?)"', lambda m: 'href="'+(m.group(1) or '')+'index.html"' if not m.group(1).startswith(('http',)) else m.group(0), doc)
    doc=doc.replace('href="./index.html"','href="index.html"')
    open(os.path.join(d,'index.html'),'w').write(doc)

def hero(img,eyebrow,h1,sub,form=False):
    f=quoteform('hero') if form else ''
    cls='hero' if form else 'hero hero-s'
    return f'''<section class="{cls}"><img src="{U(img,1920,1100)}" alt="{ALT.get('drive')}" fetchpriority="high"><div class="wrap{' two' if form else ''}"><div>
<p class="eyebrow light">{eyebrow}</p><h1>{h1}</h1><p class="sub">{sub}</p>
<div class="ctas"><a class="btn btn-red" href="{{{{R}}}}contact/">Get a free quote</a><a class="btn btn-ghost" href="{TEL}">📞 Call 07909 600964</a><a class="btn btn-wa" href="{WA}">💬 WhatsApp us</a></div>
</div>{f}</div></section>'''

def quoteform(k):
    return f'''<form class="quote-card" data-preview novalidate id="quote-{k}"><h3>Get your free quote</h3><p>Tell us about your project and we will get back to you to arrange a free visit and quote.</p>
<div class="row"><div><label>Name *</label><input name="name" required placeholder="Your name"></div><div><label>Phone *</label><input name="phone" type="tel" required placeholder="07…"></div></div>
<label>Email *</label><input name="email" type="email" required placeholder="you@example.com">
<div class="row"><div><label>Service</label><select name="service"><option>Driveway</option><option>Patio</option><option>Fencing</option><option>Turfing &amp; garden work</option><option>Other</option></select></div><div><label>Postcode *</label><input name="postcode" required placeholder="e.g. HA4"></div></div>
<label>Tell us about your project</label><textarea name="message" rows="3" placeholder="Size, current surface, what you'd like…"></textarea>
<label>Photos of the area (optional)</label><input type="file" name="photos" accept="image/*" multiple>
<button class="btn btn-red" type="submit">Send my quote request</button>
<div class="preview-note" hidden>Preview only – this staging form does not send anything. On the live site this would go to albidriveways@gmail.com and show: “Thanks – we have received your request and will be in touch soon to arrange your free quote.”</div>
<small>Prefer to talk? Call <a href="{TEL}">07909 600964</a> or <a href="{WA}">WhatsApp</a></small></form>'''

def gallery(keys,n=12,cap=None):
    items=[]
    for k in keys:
        for i in GAL[k][:n]: items.append((k,i))
    out=''.join(f'<figure><img loading="lazy" src="{U(i,800,600)}" alt="{ALT[k]}"><figcaption>{cap or ALT[k].replace(" by Albi Driveways","").replace(" laid","").replace(" installed","")}</figcaption></figure>' for k,i in items)
    return f'<div class="gal">{out}</div>'

def ba(pairs=BA):
    s=''
    for b,a,c in pairs:
        s+=f'<div class="ba-row"><h3>{c}</h3><div class="ba"><figure><img loading="lazy" src="{U(b,1000,750)}" alt="Before: {c}"><span class="tag">BEFORE</span></figure><figure><img loading="lazy" src="{U(a,1000,750)}" alt="After: {c}"><span class="tag after">AFTER</span></figure></div></div>'
    return s

def faq(items):
    return '<div class="faq">'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)+'</div>'
def faqschema(items):
    strip=lambda t: re.sub(r'<[^>]+>','',re.sub(r'<mark.*?</mark>','',t)).strip()
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in items]}
def ul(items): return '<ul class="ticks">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def ol(items): return '<ol class="steps">'+''.join(f'<li class="step"><h3>{t}</h3><p>{d}</p></li>' for t,d in items)+'</ol>'
def sec(inner,cls=''): return f'<section class="{cls}"><div class="wrap">{inner}</div></section>'
def cta(h,extra=''): return f'<div class="cta-box"><h3>{h}</h3><p>Get your free, no-obligation quote today. Call <a href="{TEL}"><b>07909 600964</b></a>, email <a href="{MAIL}"><b>albidriveways@gmail.com</b></a>, or use our <a href="{{{{R}}}}contact/">quote form</a>.{extra}</p><div class="ctas"><a class="btn btn-red" href="{{{{R}}}}contact/">Get a Free Quote</a><a class="btn btn-dark" href="{TEL}">📞 Call</a><a class="btn btn-wa" href="{WA}">💬 WhatsApp</a></div></div>'
def chips(links=None):
    links=links or {}
    return '<div class="chips">'+''.join(f'<a href="{{{{R}}}}{links[a]}" class="main">{a}</a>' if a in links else f'<span>{a}</span>' for a in AREAS)+'</div>'
TOWNLINKS={'Ruislip':'driveways-ruislip/','Eastcote':'driveways-eastcote/','Pinner':'driveways-pinner/','Northwood':'fencing-northwood/'}
G=ph('confirm guarantee length and terms')
Y=ph('confirm 27+ years')

PG=json.load(open(os.path.join(DATA,'photogrid.json')))
def pgrid(k):
    L=PG[k]
    return '<div class="pgrid" data-lb-group="'+k+'">'+''.join(f'<a href="{x["full"]}" data-lb data-id="{x["id"]}"><img loading="lazy" decoding="async" width="600" height="450" src="{U(x["full"],600,450)}" alt="{html.escape(x["alt"])}"></a>' for x in L)+'</div>'
def pgsec(k,label,cls=''):
    return sec(f'<h2>All our {label} photos <span class="count">({len(PG[k])})</span></h2><p class="lead">Every {label} photo from our own job library. Tap or click any photo to see it full size.</p>'+pgrid(k),cls)

RC=ph('confirm current Google review count – 160')
STEPSC=ph('confirm these steps match how Albi Driveways works')
def review_ph(n,what=''):
    return '<div class="grid3">'+''.join(f'<div class="rev"><div class="stars">★★★★★</div><p>{ph("add a real Google review"+what+" with first name and town")}</p><small>— Google review</small></div>' for _ in range(n))+f'</div><p style="margin-top:18px"><a class="btn btn-dark" href="{GBP}">Read our reviews on Google</a></p>'
def project_ph(k,n=6,town=''):
    return f'<p>{ph("add a real local project – captions naming the town"+(" ("+town+")" if town else "")+" and 2–3 sentences")}</p>'+gallery([k],n,cap='Location to be confirmed')

LB={"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","@id":"https://www.albidriveways.com/#business","name":"Albi Driveways","url":"https://www.albidriveways.com/","logo":LOGO,"image":U(162,1600,1200),
 "description":"Block-paving driveways, patios, fencing, turfing and garden work in Ruislip and North West London. Over 27 years' experience, Marshalls bricks, guaranteed work and free quotes.",
 "telephone":"+447909600964","email":"albidriveways@gmail.com","priceRange":"££","areaServed":[{"@type":"City","name":a} for a in AREAS],
 "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n,"url":"https://www.albidriveways.com/"+s}} for n,s in [("Block-paving driveways","driveways"),("Patios","patios"),("Fencing","fencing"),("Turfing and garden work","turfing-garden")]]},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"08:00","closes":"18:00"}],
 "sameAs":[GBP,"https://www.instagram.com/albidriveways/","https://www.facebook.com/albidriveway"]}
PH.add('opening hours in LocalBusiness schema (Mon–Sat 08:00–18:00 is a placeholder)'); PH.add('priceRange "££" in schema – confirm or remove')

# ---------- HOME
home=hero(162,'Ruislip · Eastcote · Pinner · Harrow · Watford','Driveways, Patios &amp; Fencing in <span>Ruislip and North West London</span>',
 f'Welcome to Albi Driveways. For more than 27 years {Y} we have been building block-paving driveways, patios and fencing, and laying turf, for homeowners across Ruislip and North West London. We use quality materials, including Marshalls bricks, and all our work is guaranteed {G}.',form=True)
home+=f'''<div class="trustbar"><div class="wrap"><div><b>★★★★★ Rated five stars by 160 customers on Google</b> {RC}</div><div>✓ Marshalls bricks</div><div>✓ Guaranteed work</div><div>✓ Free, no-obligation quotes</div></div></div>'''
svc=[('driveways/',9,'drive','Block-paving driveways','A new driveway makes a big difference to how your home looks and gives you somewhere safe and tidy to park. We design and lay block-paving driveways to suit your home, your space and your budget.','Driveways'),
 ('patios/',44,'patio','Patios','Get more out of your garden with a new patio for dining, relaxing or entertaining. We plan the layout with you and lay it to a neat, lasting finish.','Patios'),
 ('fencing/',29,'fence','Fencing','Good fencing gives you privacy and security and keeps your garden looking smart. We put up new fencing and replace old or storm-damaged fences.','Fencing'),
 ('turfing-garden/',14,'turf','Turfing and garden work','From a fresh new lawn to getting a tired garden back in shape, we can help with turfing and general garden work.','Turfing &amp; Garden')]
cards=''.join(f'<article class="svc"><a href="{{{{R}}}}{s}"><img loading="lazy" src="{U(i,800,600)}" alt="{ALT[k]}"></a><div class="b"><h3>{t}</h3><p>{d}</p><a href="{{{{R}}}}{s}">{l} →</a></div></article>' for s,i,k,t,d,l in svc)
home+=sec(f'<p class="eyebrow">What we do</p><h2>Our services</h2><p class="lead">Every job starts with a free, no-obligation quote, so you know exactly what you are getting before any work begins.</p><div class="grid4">{cards}</div><p class="note">Other services such as resin, tarmac, gravel, dropped kerbs or drainage are not listed. {ph("confirm whether any extra services (resin, tarmac, gravel, dropped kerbs, drainage, brickwork) are offered")}</p>')
home+=sec(f'''<div class="why"><img loading="lazy" src="{U(103,1000,750)}" alt="{ALT['drive']}"><div><p class="eyebrow">Why us</p><h2>Why homeowners choose Albi Driveways</h2>{ul([f"<b>27+ years' experience</b> {Y} – we have been doing this for a long time and it shows in the finish.","<b>Quality materials</b> – including Marshalls bricks, chosen to last.",f"<b>Guaranteed work</b> – every job is backed by our guarantee {G}.","<b>Free, no-obligation quotes</b> – clear pricing with no pressure.",f"<b>Local and trusted</b> – based in Ruislip, with five-star reviews from neighbours across the area {RC}."])}<p class="note">{ph("insurance / accreditations – add only if true (none listed yet)")}</p></div></div>''','alt')
home+=sec(f'<p class="eyebrow">Recent work</p><h2>See our work</h2><p class="lead">Have a look at our before-and-after photos to see the difference a new driveway, patio or fence can make.</p>'+gallery(['drive'],4)+gallery(['patio','fence','turf'],2)+f'<p style="margin-top:22px"><a class="btn btn-dark" href="{{{{R}}}}before-afters/">See all our work &amp; before-and-afters →</a></p>')
home+=sec(ba(BA[2:])+'','alt')
home+=sec(f'<div class="rev-head"><div><p class="eyebrow">Reviews</p><h2>What our customers say</h2></div><div class="score"><div class="n">5.0</div><div><div class="stars">★★★★★</div><div class="g">from 160 Google reviews {RC}</div></div></div></div>'+review_ph(3)+f' <a href="{{{{R}}}}reviews/">More reviews →</a>')
home+=sec(f'<div class="areas"><div><p class="eyebrow">Where we work</p><h2>Areas we cover</h2><p class="lead">We work across Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill.</p>{chips(TOWNLINKS)}<p style="margin-top:18px"><a class="btn btn-dark" href="{{{{R}}}}areas-we-cover/">See all areas →</a></p></div><img class="rimg" loading="lazy" src="{U(212,900,675)}" alt="{ALT["drive"]}"></div>','alt')
hfaq=[("Do you give free quotes?","Yes, every quote is free and there is no obligation."),("Which areas do you cover?","Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill. If you are close to these, just ask."),("What materials do you use?","We use quality materials, including Marshalls bricks."),("Is your work guaranteed?","Yes. All our work comes with our guarantee. "+G),("Can I send photos on WhatsApp?","Yes – send photos of your driveway or garden to 07909 600964. "+ph("confirm WhatsApp is used on 07909 600964"))]
home+=sec('<p class="eyebrow center">FAQ</p><h2 class="center">Common questions</h2>'+faq(hfaq))
page('', 'Driveways, Patios & Fencing Ruislip | Albi Driveways',"Block paving driveways, patios & fencing in Ruislip, Pinner, Harrow, Uxbridge & Watford. 27+ years' experience, guaranteed work. Free, no-obligation quote.",home,[LB],'')

# ---------- DRIVEWAYS
dfaq=[("How much does a new block-paving driveway cost?","It depends on the size of the area, the current surface, access and the design you choose. The best way to get an accurate price is a free, no-obligation quote. We visit, measure up and give you a clear price."),
("How long does it take to lay a driveway?","Most driveways take a few days, depending on size and the ground underneath "+ph("confirm typical driveway duration")+". We will give you a timescale with your quote."),
("Do I need permission for a new driveway?","If you need a new or wider dropped kerb, you will usually need approval from your local council. Some front-garden paving and homes in conservation areas also have extra planning rules. We will flag anything to check during your visit "+ph("confirm planning wording")+"."),
("Is your work guaranteed?","Yes. All our driveways come with our guarantee "+G+"."),("Do you give free quotes?","Yes, every quote is free and there is no obligation.")]
DK=ph('confirm what help you offer with dropped-kerb applications')
b=hero(118,'Block-paving driveways','Block-Paving Driveways in <span>Ruislip and North West London</span>',f"Your driveway is the first thing people see when they arrive at your home. A well-laid block-paving driveway gives you a smart, practical place to park and adds kerb appeal that lasts for years. At Albi Driveways we have been designing and laying block-paving driveways for more than 27 years {Y}, for homes across Ruislip, Harrow, Watford and the surrounding areas.")
b+=sec(f'''<div class="two-col"><div><h2>Why choose block paving?</h2><p>Block paving is one of the most popular choices for driveways in North West London, and for good reason:</p>{ul(["<b>Hard-wearing</b> – a properly laid block-paved driveway copes with daily parking for years.",f"<b>Looks smart</b> – a choice of colours and laying patterns lets you match the style of your home {ph('confirm range of colours/patterns offered')}.","<b>Easy to repair</b> – if a block is ever damaged, it can be lifted and replaced without redoing the whole drive.","<b>Adds value</b> – a tidy, well-designed driveway improves how your home looks from the street."])}<p>We use quality materials, including Marshalls bricks, so your driveway looks good and lasts.</p></div><img class="rimg" loading="lazy" src="{U(78,900,675)}" alt="Charcoal block-paving driveway with red border"></div>''')
b+=sec(f'<h2>How we build your driveway</h2>'+ol([("Free visit and quote","We look at the space, talk through what you want and give you a clear, no-obligation quote."),("Planning the design","We agree the shape, pattern and colours with you before work starts."),("Preparing the ground","The old surface is removed and the ground is dug out and prepared so the new driveway has a solid base."),("Laying the blocks","The blocks are laid carefully to the agreed pattern, with neat edges and cuts."),("Finishing and tidy-up","We finish the surface, clear the site and walk you through the result.")])+f'<p class="note">{STEPSC}</p>','dark')
b+=sec(f'''<h2>Planning your new driveway</h2><p>Every home is different, so it helps to think about a few things early:</p>{ul(["<b>How many cars</b> you want to park, and whether you want to keep part of the front garden.",f"<b>Access from the road</b> – if you need a new or wider dropped kerb, this usually needs approval from your local council (for example Hillingdon, Harrow, Brent, Barnet or Watford). We can talk you through it {DK}.",f"<b>Planning rules</b> – some front-garden paving and properties in conservation areas have extra rules. We will mention anything to check during your free visit {ph('confirm planning wording')}."])}<h2 style="margin-top:40px">Our guarantee</h2><p>All our driveways are backed by our guarantee, giving you peace of mind long after we have finished {G}.</p>''','alt')
b+=sec('<h2>Recent driveways</h2>'+project_ph('drive',12)+f'<p style="margin-top:18px"><a href="{{{{R}}}}before-afters/">More before-and-after photos →</a></p>')
b+=pgsec('drive','driveway')
b+=sec('<h2>What our customers say</h2>'+review_ph(2,' about a driveway'),'alt')
b+=sec(f'<h2>Areas we cover for driveways</h2><p>We lay driveways in Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill.</p><p class="links-row">Local pages: <a href="{{{{R}}}}driveways-ruislip/">Driveways in Ruislip</a> · <a href="{{{{R}}}}driveways-eastcote/">Driveways in Eastcote</a> · <a href="{{{{R}}}}driveways-pinner/">Driveways in Pinner</a> · <a href="{{{{R}}}}areas-we-cover/">All areas</a></p>')
b+=sec('<h2>Driveway FAQs</h2>'+faq(dfaq)+cta('Ready for a new driveway?'),'alt')
page('driveways','Block Paving Driveways Ruislip & Harrow | Albi Driveways',"New block-paving driveways in Ruislip, Eastcote, Northwood, Pinner, Harrow & Watford. Marshalls bricks, guaranteed work, 27+ years. Get your free quote.",b,[faqschema(dfaq)],'driveways/')

# ---------- PATIOS
pfaq=[("How much does a new patio cost?","The price depends on the size, the finish you choose, the condition of the ground and access to your garden. We will give you a free, no-obligation quote after a quick visit."),("How long does it take to lay a patio?","Most patios take a few days "+ph("confirm typical patio duration")+". We will give you a timescale with your quote."),("Can you lay a patio and turf at the same time?","Yes. We can lay a new patio and turf the rest of the garden as one job."),("Is your work guaranteed?","Yes. All our patios come with our guarantee "+G+".")]
b=hero(35,'Patios','Patio Installers in <span>Ruislip, Pinner and Harrow</span>',f"A new patio turns your garden into an extra room: somewhere to eat outside on summer evenings, relax at the weekend or have friends round. At Albi Driveways we have been designing and laying patios for more than 27 years {Y}, for homes across Ruislip, Pinner, Harrow and North West London.")
b+=sec(f'''<div class="two-col"><div><h2>A patio designed around your garden</h2><p>No two gardens are the same. We start by finding out how you want to use the space:</p>{ul(["<b>Dining and entertaining</b> – room for a table, chairs and a barbecue.","<b>Relaxing</b> – a quiet spot in the sun, or in the shade.","<b>Linking the house and garden</b> – a smooth step out from the back door or patio doors.","<b>Making a small garden work harder</b> – a neat patio can make a compact garden feel bigger and easier to look after."])}<p>We then help you choose the size, shape, layout and finish to suit your home {ph('confirm patio materials offered')}.</p></div><img class="rimg" loading="lazy" src="{U(3,900,675)}" alt="Garden patio with raised planter and timber bench"></div>''')
b+=sec('<h2>How we lay your patio</h2>'+ol([("Free visit and quote","We look at your garden, talk through your ideas and give you a clear, no-obligation quote."),("Agreeing the design","We confirm the layout and finish with you before work begins."),("Preparing the ground","The area is cleared, dug out and levelled so your patio has a solid base."),("Laying the patio","Laid carefully, with neat joints, cuts and edges."),("Finishing and tidy-up","We clean up and leave your garden ready to enjoy.")])+f'<p class="note">{STEPSC}</p>','dark')
b+=sec(f'<div class="two-col"><div><h2>Quality that lasts</h2><p>We take pride in using quality materials and careful workmanship, so your patio keeps looking good for years. All our patios are backed by our guarantee {G}.</p></div><div><h2>Patios with turf or fencing</h2><p>Many customers combine a new patio with a fresh lawn or new fencing, so the whole garden is finished at once. Doing it together usually means less disruption. <a href="{{{{R}}}}turfing-garden/">Turfing &amp; garden work</a> · <a href="{{{{R}}}}fencing/">Fencing</a></p></div></div>','alt')
b+=sec('<h2>Recent patios</h2>'+project_ph('patio',12)+f'<p style="margin-top:18px"><a href="{{{{R}}}}before-afters/">More before-and-after photos →</a></p>')
b+=pgsec('patio','patio')
b+=sec('<h2>What our customers say</h2>'+review_ph(2,' about a patio'),'alt')
b+=sec(f'<h2>Areas we cover for patios</h2><p>We lay patios in Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill. <a href="{{{{R}}}}areas-we-cover/">All areas</a></p>')
b+=sec('<h2>Patio FAQs</h2>'+faq(pfaq)+cta('Planning a new patio?'),'alt')
page('patios','Patios Ruislip, Pinner & Harrow | Albi Driveways',"Patios designed and laid across Ruislip, Ickenham, Northwood, Pinner, Harrow & Mill Hill. Neat finish, guaranteed work, 27+ years. Free quote today.",b,[faqschema(pfaq)],'patios/')

# ---------- FENCING
ffaq=[("How much does a new fence cost?","It depends on the length and height of the fence, whether old fencing needs removing and access to your garden. We will give you a free, no-obligation quote after a quick visit."),("How long does it take to put up a fence?","Most garden fences are finished in a day or two "+ph("confirm typical fencing duration")+"."),("Do I need planning permission for a new fence?","Usually not, if it is no higher than 2 metres (or 1 metre next to a road or footpath). Listed buildings and some conservation areas have extra rules "+ph("confirm planning wording")+"."),("Do you take away the old fence?",ph("confirm – e.g. “Yes, we remove and dispose of your old fencing as part of the job.”")),("Is your fencing guaranteed?","Yes. All our work comes with our guarantee "+G+".")]
b=hero(27,'Fencing','Garden Fencing in <span>Ruislip, Northwood and Uxbridge</span>',f"Good fencing does a lot of work: it gives you privacy, keeps children and pets safe, marks your boundary and frames your garden. When a fence starts to lean, rot or blow down in a storm, it is worth getting it sorted properly. At Albi Driveways we have been putting up garden fencing for homes across Ruislip, Northwood, Uxbridge and North West London for more than 27 years {Y}.")
b+=sec(f'''<div class="two-col"><div><h2>Our fencing services</h2>{ul(["<b>New fencing</b> – for new boundaries, garden makeovers or extra privacy.","<b>Fence replacement</b> – taking down old, rotten or leaning fencing and putting up new.",f"<b>Storm-damaged fences</b> – getting your garden secure again after bad weather {ph('confirm you take on storm repair/replacement call-outs')}.",f"<b>Gates</b> {ph('confirm gates are offered – remove if not')}"])}<p>We will help you choose fencing that suits your garden, your privacy needs and your budget {ph('confirm fence types offered (panels, posts, gravel boards etc.)')}.</p></div><img class="rimg" loading="lazy" src="{U(24,900,675)}" alt="New closeboard fence with concrete posts"></div>''')
b+=sec('<h2>How we put up your fence</h2>'+ol([("Free visit and quote","We look at the boundary, measure up and give you a clear, no-obligation quote."),("Removing the old fence","If needed, we take down and clear away the old fencing "+ph("confirm removal/disposal included")+"."),("Setting the posts","The posts are set firmly and in line, because a fence is only as strong as its posts."),("Fitting the fence","The fence goes up straight, level and secure."),("Tidy-up","We leave your garden clean and tidy.")])+f'<p class="note">{STEPSC}</p>','dark')
b+=sec(f'''<h2>Things to think about before you replace a fence</h2>{ul(["<b>Who owns the fence?</b> Check your property deeds, and have a quick chat with your neighbour before work starts. It saves disagreements later.",f"<b>Height</b> – in most cases a garden fence can be up to 2 metres high without planning permission, or 1 metre next to a road or footpath. Rules can differ for listed buildings and some conservation areas, so check if that applies to you {ph('confirm planning wording')}.","<b>Combining jobs</b> – if you are also planning a patio, turf or a new driveway, doing it together can save time and disruption."])}<h2 style="margin-top:40px">Guaranteed work</h2><p>All our fencing is backed by our guarantee {G}.</p>''','alt')
b+=sec('<h2>Recent fencing</h2>'+project_ph('fence',12))
b+=pgsec('fence','fencing')
b+=sec('<h2>What our customers say</h2>'+review_ph(2,' about fencing'),'alt')
b+=sec(f'<h2>Areas we cover for fencing</h2><p>We put up fencing in Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill.</p><p class="links-row">Local pages: <a href="{{{{R}}}}fencing-ruislip/">Fencing in Ruislip</a> · <a href="{{{{R}}}}fencing-northwood/">Fencing in Northwood</a> · <a href="{{{{R}}}}areas-we-cover/">All areas</a></p>')
b+=sec('<h2>Fencing FAQs</h2>'+faq(ffaq)+cta('Need a new fence?'),'alt')
page('fencing','Fencing Ruislip, Northwood & Uxbridge | Albi Driveways',"Garden fencing installed and replaced in Ruislip, Eastcote, Ickenham, Northwood, Hillingdon & Uxbridge. 27+ years, guaranteed work. Free quote.",b,[faqschema([x for x in ffaq if 'take away' not in x[0]])],'fencing/')

# ---------- TURFING
tfaq=[("When is the best time to lay turf?","Turf can be laid for much of the year, but spring and autumn are usually best, as the weather is mild and the ground is moist. We will advise on timing for your garden."),("How soon can I use my new lawn?","Give it a few weeks to root before regular use "+ph("confirm your lawn aftercare advice")+". We will give you aftercare tips on the day."),("Can you turf the garden and lay a patio at the same time?","Yes. We can do both as one project.")]
b=hero(15,'Turfing &amp; garden work','Turfing and Garden Work in <span>Ruislip and North West London</span>',f"A fresh, healthy lawn makes the whole garden look better, and gives children, pets and the rest of the family somewhere to enjoy outside. If your lawn is patchy, uneven or worn out, or the garden has just got away from you, Albi Driveways can help. We have been transforming outdoor spaces across Ruislip, Harrow and North West London for more than 27 years {Y}.")
b+=sec(f'''<div class="two-col"><div><h2>Our turfing and garden services</h2>{ul(["<b>New turf</b> – a new lawn laid on properly prepared ground.","<b>Replacing a tired lawn</b> – lifting old, patchy or weedy grass and laying fresh turf.",f"<b>Garden clearance and tidy-ups</b> – getting an overgrown garden back under control {ph('confirm garden clearance is offered')}.","<b>Complete garden makeovers</b> – combining turf with a new patio or fencing for a finished look."])}<p>{ph('confirm exact scope of garden work offered')}</p></div><img class="rimg" loading="lazy" src="{U(50,900,675)}" alt="Freshly laid turf lawn in a long back garden"></div>''')
b+=sec('<h2>How we lay new turf</h2>'+ol([("Free visit and quote","We look at the garden, talk through what you want and give you a clear, no-obligation quote."),("Clearing the area","Old grass, weeds and debris are removed "+ph("confirm")+"."),("Preparing the ground","The soil is levelled and prepared so the new turf can root well."),("Laying the turf","Laid neatly, with tight joins and clean edges."),("Aftercare advice","We tell you how to water and look after the new lawn so it establishes quickly.")])+f'<p class="note">{STEPSC}</p>','dark')
b+=sec(f'<div class="two-col"><div><h2>Looking after your new lawn</h2><p>New turf needs regular watering for the first few weeks, especially in warm or dry weather. Try to keep off it while the roots establish, and leave the first cut until the grass has taken hold. We will give you simple aftercare tips when we finish.</p></div><div><h2>Turf, patio and fencing together</h2><p>Many of our customers combine new turf with a patio or new fencing. It is a great way to get a complete, finished garden in one go, with one team and less disruption. <a href="{{{{R}}}}patios/">Patios</a> · <a href="{{{{R}}}}fencing/">Fencing</a></p></div></div>','alt')
b+=sec('<h2>Recent garden work</h2>'+project_ph('turf',10)+'<h3 style="margin-top:30px">Before &amp; after</h3>'+ba(BA[1:2]))
b+=pgsec('turf','turfing and garden')
b+=sec('<h2>What our customers say</h2>'+review_ph(2,' about turfing/garden work'),'alt')
b+=sec(f'<h2>Areas we cover</h2><p>We lay turf and carry out garden work in Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill. <a href="{{{{R}}}}areas-we-cover/">All areas</a></p>')
b+=sec('<h2>Turfing FAQs</h2>'+faq(tfaq)+cta('Want a lawn you will love?'),'alt')
page('turfing-garden','Turfing & Garden Work Ruislip & Harrow | Albi Driveways',"New lawns, turfing and garden work in Ruislip, Pinner, Harrow, Wembley & Watford. A local team with 27+ years' experience. Free, no-obligation quote.",b,[faqschema(tfaq)],'turfing-garden/')

# ---------- CONTACT
b=f'''<section class="hero hero-s"><img src="{U(128,1920,900)}" alt="Charcoal block-paving driveway"><div class="wrap two"><div><p class="eyebrow light">Free quote</p><h1>Get Your Free, <span>No-Obligation Quote</span></h1><p class="sub">Thinking about a new driveway, patio, fence or lawn? Tell us a little about your project and we will get back to you to arrange a free visit and quote {ph('confirm typical response time, e.g. “within one working day”')}.</p><p class="sub">There is no pressure and no obligation, just honest advice and a clear price.</p></div>{quoteform('contact')}</div></section>'''
b+=sec(f'''<div class="grid3"><div class="rev"><h3>Prefer to talk?</h3><p><b>Call or WhatsApp:</b> <a href="{TEL}">07909 600964</a> {ph('confirm WhatsApp is used on 07909 600964')}<br><b>Email:</b> <a href="{MAIL}">albidriveways@gmail.com</a><br><b>Hours:</b> {ph('confirm working hours (directory lists Mon–Sat 8am–6pm)')}</p><div class="ctas"><a class="btn btn-dark" href="{TEL}">📞 Call</a><a class="btn btn-wa" href="{WA}">💬 WhatsApp</a></div></div>
<div class="rev"><h3>What happens next?</h3><ol class="plain"><li><b>We get in touch</b> to talk through your project and book a convenient time to visit.</li><li><b>We visit and measure up</b>, and talk through options with you.</li><li><b>You get a clear, written quote</b> {ph('confirm quotes are written')} with no obligation.</li></ol></div>
<div class="rev"><h3>Areas we cover</h3><p>Based in Ruislip (HA4), we work across Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford and Mill Hill. <a href="{{{{R}}}}areas-we-cover/">See all areas</a></p><h3 style="margin-top:14px">Why choose us</h3><p>27+ years' experience {Y} · Marshalls bricks · Guaranteed work {G} · Rated five stars by 160 customers on Google {RC}</p></div></div>''')
page('contact','Free Driveway & Patio Quote | Contact Albi Driveways',"Request a free, no-obligation quote for a driveway, patio, fencing or turfing in Ruislip, Harrow, Uxbridge, Watford & nearby. Call or email us today.",b,None,'contact/')

# ---------- AREAS
rows=[("Ruislip (incl. Ruislip Manor &amp; South Ruislip)","HA4",'<a href="{{R}}driveways-ruislip/">Driveways in Ruislip</a> · <a href="{{R}}fencing-ruislip/">Fencing in Ruislip</a>'),("Eastcote","HA5",'<a href="{{R}}driveways-eastcote/">Driveways in Eastcote</a>'),("Ickenham","UB10","(page coming soon)"),("Northwood (incl. Northwood Hills)","HA6",'<a href="{{R}}fencing-northwood/">Fencing in Northwood</a>'),("Pinner","HA5",'<a href="{{R}}driveways-pinner/">Driveways in Pinner</a>'),("Harrow","HA1, HA2, HA3","(page coming soon)"),("Wembley","HA0, HA9","(page coming soon)"),("Hillingdon","UB8, UB10","(page coming soon)"),("Uxbridge","UB8","(page coming soon)"),("Watford","WD17, WD18, WD19, WD24, WD25","(page coming soon)"),("Mill Hill","NW7","(page coming soon)")]
tbl='<div class="tbl"><table><thead><tr><th>Area</th><th>Postcodes (main)</th><th>Local pages</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{p}</td><td>{l}</td></tr>' for a,p,l in rows)+'</tbody></table></div>'
b=hero(212,'Areas we cover','Areas We Cover in <span>North West London and Watford</span>',f"Albi Driveways is based in Ruislip (HA4), and we have been working for homeowners across North West London and the Watford area for more than 27 years {Y}. Wherever you are in the areas below, we offer the same thing: quality workmanship, Marshalls bricks, guaranteed work and a free, no-obligation quote.")
b+=sec(f'<h2>Towns and postcodes we cover</h2>{tbl}<p class="note">{ph("confirm postcode lists and that you work in all 11 areas regularly")}</p>')
b+=sec(f'<div class="two-col"><div><h2>Our services in every area</h2>{ul(["<b>Block-paving driveways</b> – <a href=\"{{R}}driveways/\">Driveways</a>","<b>Patios</b> – <a href=\"{{R}}patios/\">Patios</a>","<b>Fencing</b> – <a href=\"{{R}}fencing/\">Fencing</a>","<b>Turfing and garden work</b> – <a href=\"{{R}}turfing-garden/\">Turfing &amp; Garden</a>"])}</div><div><h2>Local knowledge</h2><p>Working locally for so long means we know the area. Many homes around Ruislip, Eastcote and Pinner are 1920s and 1930s semi-detached and terraced houses, where the front garden is often turned into a driveway. Northwood and parts of Pinner have larger detached homes with bigger gardens. Harrow, Wembley and Watford have a real mix. Whatever your home, we will design a driveway, patio or fence that suits it.</p></div></div>','alt')
b+=sec(f'<div class="mapbox">{ph("optional: embed a map of the service area")}</div><h2 style="margin-top:36px">Not sure if we cover you?</h2><p>If your area is close to the ones listed, just ask. Call <a href="{TEL}"><b>07909 600964</b></a> or email <a href="{MAIL}"><b>albidriveways@gmail.com</b></a>.</p><p style="margin-top:16px"><a class="btn btn-red" href="{{{{R}}}}contact/">Get a Free Quote</a></p>')
page('areas-we-cover','Areas We Cover – Ruislip to Watford | Albi Driveways',"Driveways, patios, fencing and turfing in Ruislip, Eastcote, Ickenham, Northwood, Pinner, Harrow, Wembley, Hillingdon, Uxbridge, Watford & Mill Hill.",b,None,'areas-we-cover/')

# ---------- TOWN PAGES
def town(slug,title,desc,h1,img,k,intro,blocks,local,town_,why,also,nearby,svc,svctype):
    b=hero(img,f'{town_} · local page',h1,intro)
    for h,c in blocks: b+=sec(f'<h2>{h}</h2>{c}')
    b+=sec(f'<h2>Local things to think about</h2>{ul(local)}','alt')
    b+=sec(f'<h2>Recent {"driveway" if k=="drive" else "fencing"} in {town_}</h2>'+project_ph(k,6,town_))
    b+=sec(f'<h2>What {town_} customers say</h2>'+review_ph(1,f" from {'an' if town_[0] in 'AEIOU' else 'a'} {town_} customer"),'alt')
    b+=sec(f'<h2>{why}</h2>{ul([f"Local team, based in Ruislip {ph(chr(39)+"confirm Ruislip (HA4) base can be shown publicly"+chr(39)) if False else ""}".strip(), f"More than 27 years’ experience {Y}.", f"Guaranteed work {G} and free, no-obligation quotes.", f"Rated five stars by 160 customers on Google {RC}."])}<p>{also}</p>')
    b+=sec(cta(f'Get a free {"driveway" if k=="drive" else "fencing"} quote in {town_}.')+f'<h3 style="margin-top:30px">Nearby areas</h3><p class="links-row">{nearby}</p>','alt')
    sch={"@context":"https://schema.org","@type":"Service","name":svc,"serviceType":svctype,"url":"https://www.albidriveways.com/"+slug,"provider":{"@id":"https://www.albidriveways.com/#business"},"areaServed":{"@type":"City","name":town_}}
    page(slug,title,desc,b,[sch],'areas-we-cover/')
CA=lambda: ph('confirm conservation-area wording')
town('driveways-ruislip','Driveways Ruislip | Block Paving HA4 | Albi Driveways',"Block-paving driveways in Ruislip HA4 from a local Ruislip team with 27+ years' experience. Marshalls bricks, guaranteed work. Get your free quote today.",'Block-Paving Driveways in <span>Ruislip</span>',139,'drive',
 f"Ruislip is home for Albi Driveways. We are based here in HA4 and have spent more than 27 years {Y} laying block-paving driveways for neighbours across Ruislip, Ruislip Manor and South Ruislip. If you are looking for a local driveway company that knows the area and takes pride in the finish, we would love to help.",
 [("Driveways that suit Ruislip homes","<p>Much of Ruislip was built in the 1920s and 1930s, when the Metropolitan line arrived and “Metro-land” estates spread out from the High Street and Ruislip Manor. Many of those semi-detached and terraced houses were built before most families owned cars. Today their front gardens are often turned into driveways, or older drives are extended to fit a second car.</p><p>A block-paving driveway is a great fit for these homes. You can choose a colour and pattern that suits the brickwork of a 1930s semi, and keep a planted border to soften the front of the house. We use quality materials, including Marshalls bricks, so it looks good for years.</p>")],
 [f"<b>Dropped kerbs:</b> Ruislip is in the London Borough of Hillingdon. If you need a new or wider dropped kerb (vehicle crossover), you will usually need the council's approval first. We can talk you through it {DK}.",f"<b>Conservation areas:</b> Parts of Ruislip, including around the old village near St Martin's Church and Manor Farm, are in conservation areas {CA()}. Extra rules can apply there, so check before planning major front-garden changes.","<b>Trees and verges:</b> Many Ruislip roads are tree-lined with grass verges. We will plan your driveway around existing trees and the access to the road."],
 'Ruislip','Why choose a local Ruislip driveway company?','We also lay patios, put up fencing and lay turf in Ruislip. See our <a href="{{R}}fencing-ruislip/">Fencing in Ruislip</a> page, or our <a href="{{R}}patios/">Patios</a> and <a href="{{R}}turfing-garden/">Turfing</a> services.',
 '<a href="{{R}}driveways-eastcote/">Driveways in Eastcote</a> · <a href="{{R}}driveways-pinner/">Driveways in Pinner</a> · Ickenham · Northwood · <a href="{{R}}areas-we-cover/">All areas</a>','Block-paving driveways in Ruislip','Block-paving driveway installation')
town('driveways-eastcote','Driveways Eastcote | Block Paving HA5 | Albi Driveways',"Block-paving driveways in Eastcote HA5, just next door to our Ruislip base. 27+ years' experience, Marshalls bricks, guaranteed work. Free quote today.",'Block-Paving Driveways in <span>Eastcote</span>',82,'drive',
 f"Eastcote sits right next door to our Ruislip base, so we are often working on driveways around Field End Road, Eastcote village and the roads between Eastcote and Northwood Hills. If you want a smart, hard-wearing block-paving driveway from a local team with more than 27 years' experience {Y}, Albi Driveways is here to help.",
 [("Driveways for Eastcote's 1930s homes","<p>Like much of this part of Hillingdon, Eastcote grew quickly in the 1930s after the Metropolitan and Piccadilly line station opened. Many roads are lined with semi-detached houses with bay windows, often with a front garden that is just big enough for a car or two.</p><p>That makes Eastcote a perfect place for a well-designed block-paving driveway. A good design can:</p>"+ul(["give you <b>off-street parking for one or two cars</b>,","<b>keep some planting</b> at the front so the house still looks welcoming,","<b>match the style of the house</b>, with colours that suit 1930s brickwork."])+"<p>We use quality materials, including Marshalls bricks.</p>")],
 [f"<b>Dropped kerbs:</b> Eastcote is in the London Borough of Hillingdon. A new or wider dropped kerb usually needs council approval {DK}.",f"<b>Conservation areas:</b> Parts of Eastcote, such as Eastcote Village and the area around Eastcote House Gardens, are in conservation areas {CA()}. Check any extra rules before changing your front garden.","<b>Shared and narrow frontages:</b> Many semis have narrow frontages next to a neighbour's drive. We plan the edges and levels carefully so your new driveway sits neatly alongside next door."],
 'Eastcote','Why Eastcote homeowners choose us','We also lay patios, put up fencing and lay turf in Eastcote: see <a href="{{R}}patios/">Patios</a>, <a href="{{R}}fencing/">Fencing</a> and <a href="{{R}}turfing-garden/">Turfing</a>.',
 '<a href="{{R}}driveways-ruislip/">Driveways in Ruislip</a> · <a href="{{R}}driveways-pinner/">Driveways in Pinner</a> · Northwood · <a href="{{R}}areas-we-cover/">All areas</a>','Block-paving driveways in Eastcote','Block-paving driveway installation')
town('driveways-pinner','Driveways Pinner | Block Paving HA5 | Albi Driveways',"Block-paving driveways in Pinner HA5, from period homes to 1930s semis. 27+ years' experience, Marshalls bricks, guaranteed work. Get your free quote.",'Block-Paving Driveways in <span>Pinner</span>',103,'drive',
 f"Pinner has a character all of its own, from the historic High Street with its timber-framed buildings to the leafy roads around Pinner Memorial Park and Pinner Hill. Albi Driveways has been laying block-paving driveways across this part of North West London for more than 27 years {Y}, and we enjoy creating driveways that fit Pinner's mix of homes.",
 [("A driveway that suits your Pinner home","<p>Pinner has a wide range of houses:</p>"+ul(["<b>1930s semi-detached houses</b> around Rayners Lane, Pinner Green and North Harrow, where the front garden is often converted to parking.","<b>Larger detached homes</b> towards Pinner Hill and Hatch End, where a wider driveway may need to fit several cars and a turning space.","<b>Older period properties</b> near the village centre, where a more traditional look often suits best."])+f"<p>Block paving works well for all of these, because you can choose colours and laying patterns to match the house {ph('confirm range of colours/patterns offered')}. We use quality materials, including Marshalls bricks.</p>")],
 [f"<b>Harrow Council:</b> Pinner is in the London Borough of Harrow. A new or wider dropped kerb usually needs the council's approval {DK}.",f"<b>Conservation areas:</b> Pinner has several conservation areas, including the High Street and parts of the surrounding roads {CA()}. If your home is in one, check any extra rules before changing the front garden.","<b>Larger and sloping plots:</b> Some Pinner driveways are long or sit on a slope. We plan levels and edges carefully so the finished drive looks neat and works well day to day."],
 'Pinner','Why choose Albi Driveways in Pinner?','We also lay patios and put up fencing in Pinner: see <a href="{{R}}patios/">Patios</a> and <a href="{{R}}fencing/">Fencing</a>.',
 '<a href="{{R}}driveways-eastcote/">Driveways in Eastcote</a> · <a href="{{R}}driveways-ruislip/">Driveways in Ruislip</a> · Northwood · Harrow · <a href="{{R}}areas-we-cover/">All areas</a>','Block-paving driveways in Pinner','Block-paving driveway installation')
town('fencing-ruislip','Fencing Ruislip | Garden Fences HA4 | Albi Driveways',"New and replacement garden fencing in Ruislip HA4 from a local team with 27+ years' experience. Guaranteed work and free, no-obligation quotes. Call today.",'Garden Fencing in <span>Ruislip</span>',25,'fence',
 f"Albi Driveways is based in Ruislip, and fencing is one of the jobs our neighbours here ask us about most. Whether you need a brand-new boundary, want more privacy in the back garden or have a fence that has finally given up after a windy winter, we can help. We have more than 27 years' experience {Y} working on gardens across Ruislip, Ruislip Manor and South Ruislip.",
 [("Fencing for Ruislip gardens","<p>Many Ruislip homes have long, narrow back gardens with fences shared with neighbours on both sides, and often another boundary at the end of the garden. Over time, posts rot and panels lean or blow down. Replacing them properly gives you a straight, secure fence that lasts.</p><p>We offer:</p>"+ul(["<b>New fencing</b> for new boundaries and garden makeovers.","<b>Fence replacement</b> for old, rotten or leaning fences.",f"<b>Storm-damage replacement</b> to get your garden secure again {ph('confirm you take on storm repair/replacement call-outs')}."])+f"<p>We will help you choose fencing that suits your garden and your budget {ph('confirm fence types offered (panels, posts, gravel boards etc.)')}.</p>")],
 ["<b>Talk to your neighbours:</b> With so many shared boundaries in Ruislip's semis and terraces, it is worth agreeing the plan with your neighbour before work starts, and checking your deeds for who owns which fence.",f"<b>Height:</b> A garden fence can usually be up to 2 metres without planning permission, or 1 metre next to a road or footpath {ph('confirm planning wording')}. Homes in Ruislip's conservation areas may have extra rules {CA()}.","<b>Gardens backing onto woods and open space:</b> Gardens near Ruislip Woods, Park Wood or the Lido can face more wind and wildlife, so a solidly built fence matters even more."],
 'Ruislip','Why choose us for fencing in Ruislip?','Planning more garden work? We also lay <a href="{{R}}patios/">patios</a> and <a href="{{R}}turfing-garden/">turf</a>, and build <a href="{{R}}driveways-ruislip/">driveways in Ruislip</a>.',
 '<a href="{{R}}fencing-northwood/">Fencing in Northwood</a> · Eastcote · Ickenham · <a href="{{R}}areas-we-cover/">All areas</a>','Garden fencing in Ruislip','Fencing installation')
town('fencing-northwood','Fencing Northwood | Garden Fences HA6 | Albi Driveways',"Garden fencing installed and replaced in Northwood and Northwood Hills HA6. Local team, 27+ years' experience, guaranteed work. Free, no-obligation quote.",'Garden Fencing in <span>Northwood</span>',28,'fence',
 f"Northwood is one of the greenest corners of North West London, surrounded by Copse Wood, Ruislip Woods and open countryside towards Moor Park. Many homes here have generous gardens and long boundaries, so good, solid fencing really matters. Albi Driveways is based just down the road in Ruislip and has more than 27 years' experience {Y} working on gardens across Northwood and Northwood Hills.",
 [("Fencing for Northwood's larger gardens","<p>Northwood has many large detached and semi-detached homes, often from the early and mid-twentieth century, with big back gardens. That usually means:</p>"+ul(["<b>Longer runs of fencing</b>, sometimes on more than one side of the garden.","<b>More exposure to wind</b>, especially for gardens backing onto woodland or open ground.","<b>Privacy</b> between neighbouring gardens and from nearby paths."])+f"<p>We put up new fencing, replace old or leaning fences, and help after storm damage {ph('confirm you take on storm repair/replacement call-outs')}. We will help you choose fencing that suits your garden and budget {ph('confirm fence types offered (panels, posts, gravel boards etc.)')}.</p>")],
 ["<b>Woodland edges:</b> If your garden backs onto Copse Wood, Ruislip Woods or other green space, a well-built fence helps keep your garden secure and private. Posts need to be set firmly to cope with exposed spots.",f"<b>Trees:</b> Mature trees are common in Northwood gardens. We plan fence lines around roots and trees. Some trees in the area may have Tree Preservation Orders, so check with Hillingdon Council if you are unsure {ph('confirm TPO wording')}.",f"<b>Height and conservation areas:</b> A garden fence can usually be up to 2 metres without planning permission, or 1 metre next to a road or footpath. Parts of Northwood are in conservation areas, where extra rules may apply {CA()}."],
 'Northwood','Why choose Albi Driveways in Northwood?','We also lay <a href="{{R}}patios/">patios</a>, <a href="{{R}}turfing-garden/">turf</a> and <a href="{{R}}driveways/">block-paving driveways</a> in Northwood.',
 '<a href="{{R}}fencing-ruislip/">Fencing in Ruislip</a> · Eastcote · Pinner · <a href="{{R}}areas-we-cover/">All areas</a>','Garden fencing in Northwood','Fencing installation')

# ---------- BEFORE-AFTERS / OUR WORK
b=hero(205,'Our work','Our Work &amp; <span>Before-and-Afters</span>','Real jobs by Albi Driveways, taken from our own photo library: block-paving driveways, patios, fencing and new lawns.')
b+=sec('<h2>Before &amp; after</h2>'+ba()+f'<p class="note">{ph("add more real before/after pairs with town captions")}</p>')
for k,h in [('drive','Driveways'),('patio','Patios'),('fence','Fencing'),('turf','Turfing &amp; gardens')]:
    b+=sec(f'<h2>{h}</h2>'+gallery([k],16),'alt' if k in('patio','turf') else '')
b+=sec(f'<h2>Other job photos <span class="count">({len(PG["ourwork"])})</span></h2><p class="lead">More photos from our job library, mostly taken before work started. Tap or click any photo to see it full size.</p>'+pgrid('ourwork'),'alt')
page('before-afters','Our Work & Before-and-Afters | Albi Driveways','Photos of real driveways, patios, fencing and turfing jobs by Albi Driveways across Ruislip, North West London and Watford.',b,None,'before-afters/')

# ---------- REVIEWS
b=hero(9,'Reviews','What Our <span>Customers Say</span>',f'Albi Driveways is rated 5.0 on Google, from 160 reviews {RC}.')
b+=sec(f'<div class="rev-head"><h2>Google reviews</h2><div class="score"><div class="n">5.0</div><div><div class="stars">★★★★★</div><div class="g">from 160 Google reviews {RC}</div></div></div></div>'+review_ph(6)+f'<p class="note">{ph("replace the broken Trustmary widget with a working Google reviews embed, or keep hand-picked quotes")}</p>')
page('reviews','Reviews | Albi Driveways','Read what customers across Ruislip, Eastcote, Harrow and North West London say about Albi Driveways on Google.',b,None,'reviews/')

# ---------- BRICKWORK (optional, unconfirmed)
bfaq=[("Can you build brick steps as part of a new patio?","Yes. We can design and build brick steps at the same time as your patio, so everything matches "+ph("confirm")+"."),("Do I need planning permission for a garden wall?","Usually not for a low garden wall. In most cases a wall up to 2 metres high needs no planning permission, or 1 metre next to a road or footpath. Listed buildings and some conservation areas have extra rules "+ph("confirm planning wording")+"."),("Is your brickwork guaranteed?","Yes. Our work comes with our guarantee "+G+".")]
b=f'<div class="warnbar">{ph("OPTIONAL PAGE – brickwork is NOT confirmed by the owner. Publish only if Algen confirms brickwork is offered.")}</div>'
b+=hero(47,'Brickwork','Brickwork in <span>Ruislip and North West London</span>',f"Good brickwork adds structure and character to any outdoor space. Whether you need steps between garden levels, a low wall around a patio or a neat brick border, Albi Driveways can build it to a high standard. Based in Ruislip, we have more than 27 years' experience {Y} transforming outdoor spaces across North West London, and brickwork is often the finishing touch that pulls a project together {ph('confirm')}.")
b+=sec(f'<div class="two-col"><div><h2>Our brickwork services {ph("confirm full list")}</h2>{ul(["<b>Brick steps</b> – solid, safe steps from the house to the garden or between levels, built to suit your patio and home.",f"<b>Garden walls</b> – low walls to frame a patio or lawn, divide the garden or create raised beds {ph('confirm wall types and heights')}.","<b>Brick edging</b> – crisp borders for patios, paths and lawns.",f"<b>Driveway brickwork</b> – brick piers, entrance walls or edging to finish a new driveway {ph('confirm')}."])}</div><div><h2>Built to match your home</h2><p>Many homes around Ruislip, Eastcote and Pinner are 1920s and 1930s houses with distinctive brickwork. We aim to choose bricks and finishes that sit comfortably alongside your house, so new work looks like it belongs {ph("confirm how bricks are chosen/matched")}. Where it suits, we use quality materials, including Marshalls bricks.</p></div></div>')
b+=sec('<h2>How we work</h2>'+ol([("Free visit and quote","We look at the space, talk through what you want and give you a clear, no-obligation quote."),("Agreeing the design","Size, shape, brick and finish are confirmed with you before work starts."),("Groundwork","The area is prepared so the brickwork has a solid base "+ph("confirm")+"."),("Building","Laid in neat, level courses with tidy pointing."),("Tidy-up","We clear away and leave everything clean.")])+f'<p class="note">{STEPSC}</p>','dark')
b+=sec('<h2>Recent brickwork</h2>'+project_ph('brick',9)+f'<p>Brickwork works best planned together with a new patio or driveway, so steps, walls and edging all match. See our <a href="{{{{R}}}}patios/">Patios</a> and <a href="{{{{R}}}}driveways/">Driveways</a> pages.</p>')
b+=pgsec('brick','brickwork')
b+=sec('<h2>Brickwork FAQs</h2>'+faq(bfaq)+cta('Planning steps, a wall or other brickwork?'),'alt')
page('brickwork','Brickwork Ruislip | Brick Steps & Walls | Albi Driveways',"Brick steps, garden walls and brick edging in Ruislip, Pinner, Harrow & North West London. 27+ years' experience, guaranteed work. Free quote.",b,None,'')

open(os.path.join(OUT,'robots.txt'),'w').write("User-agent: *\nDisallow: /\n")
json.dump(sorted(PH),open(os.path.join(DATA,'placeholders.json'),'w'),indent=1,ensure_ascii=False)
print(len(PH),'placeholders')
