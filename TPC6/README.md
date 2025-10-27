### Parser para expressões aritméticas (Recursivo Descendente)

[Resolução](https://github.com/jlfmendes32/PLC2025/blob/main/TPC5/parser.py)

Resumo:

Construiu-se um parser usando a seguinte gramática:

p1: Exp → T ExpL
p2: ExpL → Op T
p3:      | eps
p4: T → F ExpL
p5: F → num
p6:   | '(' Exp ')'

E tomando por base o exemplo disponibilizado na Blackboard.

João Mendes, pg60226

<img src="https://github.com/user-attachments/assets/9eab7434-fb2c-43ef-bbc4-4d3f88e145fc" width="180">