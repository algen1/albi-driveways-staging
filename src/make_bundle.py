"""Pack dist/ into the text bundle format used by the Wix MCP tool UploadHeadlessWebsiteFiles.

Usage:  python3 src/make_bundle.py      -> writes build/upload-bundle.txt (git-ignored)
Each file becomes a section starting with a line `=== FILE: <path> ===`.
The bundle always contains the FULL site, because every upload replaces everything on the site.
"""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST=os.path.join(ROOT,'dist')
assert os.path.isfile(os.path.join(DIST,'index.html')), 'run python3 src/build.py first'
out=[]
for root,ds,fs in os.walk(DIST):
    ds.sort()
    for f in sorted(fs):
        full=os.path.join(root,f); rel=os.path.relpath(full,DIST).replace(os.sep,'/')
        out.append(f'=== FILE: {rel} ===\n'+open(full,encoding='utf-8').read().rstrip('\n')+'\n')
os.makedirs(os.path.join(ROOT,'build'),exist_ok=True)
dst=os.path.join(ROOT,'build','upload-bundle.txt')
open(dst,'w',encoding='utf-8').write(''.join(out))
print(len(out),'files ->',dst,os.path.getsize(dst),'bytes')
