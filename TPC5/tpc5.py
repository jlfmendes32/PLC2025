import sys
import ply.lex as lex
import json
from datetime import datetime
import re

with open('TPC5/stock.json', 'r',encoding='utf-8') as f:
    data = json.load(f)

saldo=0.0

states = (
    ('moedas', 'exclusive'),
    ('selecionar', 'exclusive'), # num estado exclusivo, apenas aplicamos os tokens e regras para esse estado
                           # por outro lado, num estado inclusivo, as regras e tokens desse estado juntam-se às outras regras e tokens
                           # o estado inicial chama-se 'INITIAL' e não é preciso defini-lo
)

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'coins',
    'COD'
)


t_ignore = ' \t\n' # estes tokens apenas são ignorados no estado 'INITIAL' e em estados inclusivos
t_moedas_ignore=' \t\n,'
t_selecionar_ignore=' \t\n'

def t_LISTAR(r):
   r'LISTAR'
   print("maq:")
   print(f"{'cod':^6} | {'nome':^20} | {'quant':^10} | {'preço':^8}")
   print("-" * 52)

   for linha in data:
        print(f"{linha['cod']:^6} | {linha['nome']:^20} | {linha['quant']:^10} | {linha['preco']:^8}")

   return r

def dar_troco(saldo):
    if saldo <= 0:
        return "sem troco."

    moedas = [200, 100, 50, 20, 10, 5, 2, 1]
    troco = int(round(saldo))
    partes = []

    for moeda in moedas:
        qtd, troco = divmod(troco, moeda)
        if qtd:
            if moeda >= 100:
                partes.append(f"{qtd}x {moeda // 100}€")
            else:
                partes.append(f"{qtd}x {moeda}c")

    if len(partes) > 1:
        return ', '.join(partes[:-1]) + ' e ' + partes[-1] + '.'
    else:
        return partes[0] + '.'

def t_SAIR(t):
    r'SAIR'
    global saldo
    troco_str = dar_troco(saldo)
    print(f"maq: Pode retirar o troco: {troco_str}")
    print("maq: Até à próxima")
    saldo = 0.0
    t.lexer.sair = True
    return t

def t_SELECIONAR(r):
    r'SELECIONAR'
    r.lexer.begin('selecionar')

def t_selecionar_COD(r):
    r'[A-Z]+(\d+)'
    i=-1
    global saldo
    m=re.match(r'[A-Z]+(\d+)',r.value)
    for n in m.groups(0):
        i+=int(n)
    p=data[i]["preco"]*100
    if data[i]["quant"] > 0:
        if p < saldo:
            saldo-=p
            data[i]["quant"]-=1
            with open('TPC5/stock.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"maq: Pode retirar o produto dispensado {data[i]["nome"]}")
            print(f"Saldo = {int(int(saldo/100))}e{int(saldo)%100}c; Pedido={int(int(p/100))}e{int(p)%100}c ")
        else:
            print("maq: Saldo insuficiente para satisfazer o seu pedido")
    else :
        print("Não há produto")


def t_MOEDA(r):
    r'MOEDA'
    r.lexer.begin('moedas')

    
def t_moedas_coins(r):
    r'\d+(e|c)'
    global saldo
    m = re.match(r'(\d+)([ec])', r.value)
    if m:
        valor, tipo = m.groups()
        valor=int(valor)
        if tipo == 'e':
            saldo+=valor*100
        else:
            saldo+=valor
    return r



def t_ANY_error(t): # regra válida para todos os estados
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.begin('INITIAL')
    t.lexer.skip(1)
    return t



lexer = lex.lex()
lexer.sair = False

#################



date_time = datetime.now().strftime("%Y/%m/%d")
print(f"maq: {date_time}, Stock carregado, Estado atualizado")
print("maq: Bom dia. Estou disponível para atender o seu pedido")

while True:
    try:
        texto = input('>> ')
    except EOFError:
        break

    lexer.input(texto)

    teve_moedas = False
    for tok in lexer:
        if tok.type in ('MOEDA', 'coins'):
            teve_moedas = True
        
        
    if teve_moedas:
         print(f"saldo={int(int(saldo/100))}e{int(saldo)%100}c")
    tok.lexer.begin('INITIAL')
    if lexer.sair:
        break
