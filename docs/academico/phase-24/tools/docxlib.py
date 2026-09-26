import re
def split_blocks(body):
    """Split a WordprocessingML body fragment into top-level blocks."""
    i=0; items=[]
    start=re.compile(r'<(w:p|w:tbl|w:sdt|w:bookmarkStart|w:bookmarkEnd)(?=[\s/>])')
    while True:
        m=start.search(body,i)
        if not m:
            break
        if m.start()>i and body[i:m.start()].strip():
            items.append(('raw',body[i:m.start()]))
        tag=m.group(1)
        if tag.startswith('w:bookmark'):
            e=body.index('>',m.start())+1; items.append((tag,body[m.start():e])); i=e; continue
        pat=re.compile(r'<(/?)'+tag+r'(?=[\s/>])([^>]*?)(/?)>')
        depth=0; j=None
        for mm in pat.finditer(body,m.start()):
            if mm.group(3)=='/':
                if depth==0: j=mm.end(); break
                continue
            if mm.group(1)=='': depth+=1
            else:
                depth-=1
                if depth==0: j=mm.end(); break
        assert j, (tag, m.start())
        items.append((tag,body[m.start():j])); i=j
    if body[i:].strip(): items.append(('raw',body[i:]))
    return items
def txt(x): return ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>',x))
