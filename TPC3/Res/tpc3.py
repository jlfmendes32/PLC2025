
import sys
import re

def tokenize(input_string,linha):
    reconhecidos = []
    mo = re.finditer(r'(?P<S>SELECT)|(?P<W>WHERE)|(?P<VAR>\?\w+)|(?P<ID>\w*:\w+)|(?P<PONTO>\.)|(?P<PA>\{)|(?P<PF>\})|(?P<SKIP>[ \t])|(?P<NEWLINE>\n)|(?P<ERRO>.)', input_string)
    for m in mo:
        dic = m.groupdict()
        if dic['S']:
            t = ("S", dic['S'], linha, m.span())

        elif dic['W']:
            t = ("W", dic['W'], linha, m.span())
    
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())
    
        elif dic['ID']:
            t = ("ID", dic['ID'], linha, m.span())
    
        elif dic['PONTO']:
            t = ("PONTO", dic['PONTO'], linha, m.span())
    
        elif dic['PA']:
            t = ("PA", dic['PA'], linha, m.span())
    
        elif dic['PF']:
            t = ("PF", dic['PF'], linha, m.span())
    
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())
    
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
    
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())
    
        else:
            t = ("UNKNOWN", m.group(), linha, m.span())
        if not dic['SKIP'] and t[0] != 'UNKNOWN': reconhecidos.append(t)
    return reconhecidos

l=1
for linha in sys.stdin:
    for tok in tokenize(linha,l):
        print(tok)
    l+=1    

