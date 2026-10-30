# Usage: python3 src/linkcheck.py http://localhost:8080/   (or the staging URL)
# Crawls internal pages, checks every internal/external link and image, and flags pages missing noindex or the STAGING ribbon.
# Note: the fonts.googleapis.com / fonts.gstatic.com preconnect URLs return 404 when fetched bare; that is expected and harmless.
import re,sys,urllib.request,urllib.parse,concurrent.futures as cf
base=sys.argv[1].rstrip('/')+'/'
seen=set();todo=[base];internal={};external=set();pages=0;problems=[]
def get(u):
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 linkcheck'}),timeout=30);return r.status,r.read(),r.headers.get('content-type','')
while todo:
    u=todo.pop()
    if u in seen: continue
    seen.add(u)
    try: st,body,ct=get(u)
    except Exception as e: internal[u]=str(e);continue
    internal[u]=st
    if 'html' not in ct: continue
    pages+=1;h=body.decode()
    if '<meta name="robots" content="noindex, nofollow">' not in h: problems.append('no noindex '+u)
    if 'STAGING PREVIEW' not in h: problems.append('no ribbon '+u)
    for a in re.findall(r'(?:href|src)="([^"]+)"',h):
        if a.startswith(('tel:','mailto:','#')): continue
        full=urllib.parse.urljoin(u,a).split('#')[0]
        if full.startswith(base): todo.append(full)
        else: external.add(full)
def chk(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30);return u,r.status
    except Exception as e: return u,str(e)
with cf.ThreadPoolExecutor(16) as ex: ext=list(ex.map(chk,sorted(external)))
bad_i=[(u,s) for u,s in internal.items() if s!=200]
bad_e=[(u,s) for u,s in ext if s!=200]
print('pages',pages,'internal urls',len(internal),'bad',bad_i)
print('external urls',len(ext),'wixstatic',sum('wixstatic' in u for u,_ in ext),'bad',bad_e)
print('problems',problems)
