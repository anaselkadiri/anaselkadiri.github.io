import pikepdf, re, sys
SRC='/mnt/user-data/outputs/anas-portfolio/assets/CV_Anas_El_Kadiri_sans_QR.pdf'
def cmap(font):
    tu=font.ToUnicode.read_bytes().decode('latin1'); m={}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar',tu,re.S):
        for a,b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>',blk): m[int(a,16)]=bytes.fromhex(b).decode('utf-16-be')
    for blk in re.findall(r'beginbfrange(.*?)endbfrange',tu,re.S):
        for a,b,c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>',blk):
            for i in range(int(a,16),int(b,16)+1): m[i]=chr(int(c,16)+i-int(a,16))
    return m
def blocks(pdf,pi):
    pg=pdf.pages[pi]; fm={k:cmap(v) for k,v in pg.Resources.Font.items()}
    ops=pikepdf.parse_content_stream(pg); out=[]; cur=None; font=None;size=None;pos=None
    for idx,(operands,op) in enumerate(ops):
        o=str(op)
        if o=='BDC' and len(operands)>1 and isinstance(operands[1],pikepdf.Dictionary) and '/MCID' in operands[1]:
            cur=dict(mcid=int(operands[1].MCID),start=idx,text='',x=None,y=None,font=None,size=None)
        elif o=='Td' and cur is not None: cur['x'],cur['y']=float(operands[0]),float(operands[1])
        elif o=='Tf' and cur is not None: cur['font']=str(operands[0]);cur['size']=float(operands[1])
        elif o in('Tj','TJ') and cur is not None:
            items=[operands[0]] if o=='Tj' else [x for x in operands[0] if isinstance(x,pikepdf.String)]
            for s in items: cur['text']+=''.join(fm[cur['font']].get(b,'?') for b in bytes(s))
        elif o=='EMC' and cur is not None:
            cur['end']=idx; out.append(cur); cur=None
    return out
if __name__=='__main__':
    pdf=pikepdf.open(SRC)
    for pi in range(len(pdf.pages)):
        print('=== PAGE',pi)
        for b in blocks(pdf,pi):
            if b['text'].strip(): print(b['mcid'],b['start'],b['end'],round(b['x'] or 0,1),round(b['y'] or 0,1),b['font'],b['size'],repr(b['text'][:110]))
