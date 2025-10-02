import re
import sys


cabe=re.compile(r'(?P<cabeçalho>^(#*)\s*(.*))')
im=re.compile(r'(?P<img>!\[(.*)\]\((.*)\))')
bold=re.compile(r'(?P<bold>\*\*(.*)\*\*)')
ita=re.compile(r'(?P<ita>\*(.*)\*)')
lik=re.compile(r'(?P<link>\[(.*)\]\((.*)\))')
ListaNum=re.compile(r'(?P<lista>((\d+\.)\s*(.+)+))')

def cabesub(m):
    nh=len(m.group(2))
    return rf"<h{nh}>{m.group(3)}</h{nh}>"


def converte(t):
    i=0
    t=re.sub(cabe,cabesub,t)
    t=re.sub(bold,r"<b>\2</b>",t)
    t=re.sub(ita,r"<i>\2</i>",t)
    t=re.sub(im,r'<img src="\3" alt="\2"/>',t)
    t=re.sub(lik,r'<a href="\3">\2</a>',t)
    t=re.split("\n",t)
    tamanho=len(t)
    while (i<tamanho):
        if re.match(ListaNum,t[i]):
            t[i-1]=t[i-1]+"\n<ol>"
            while(re.match(ListaNum,t[i]) and i< tamanho):
                t[i]=re.sub(ListaNum,r"<li>\4</li>",t[i])
                i+=1
            t[i]=t[i]+"</ol>\n"
        else:    
            i+=1

    t="\n".join(t)
    return t

def read_input():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return sys.stdin.read()

def main():
    text = read_input()
    out = converte(text)
    sys.stdout.write(out)

if __name__ == "__main__":
    main()


