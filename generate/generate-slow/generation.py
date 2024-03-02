from random import *
from sys import argv

class Expr:
    def __init__(self, type, name):
        self.type = type
        assert(type in ["N", "T", ";", "/", "*", "!"])
        if type == "N":
            self.no_kids = 0
            self.name = name
        elif type == "T":
            self.no_kids = 0
            self.name = name
        elif type == ";":
            self.no_kids = 2
        elif type == "/":
            self.no_kids = 2
        elif type == "*":
            self.no_kids = 1
        elif type == "!":
            self.no_kids = 1
        self.kids = [[] for _ in range(self.no_kids)]

    def __repr__(self):
        if self.type in ["N", "T"]:
            return self.name
        return self.type + "(" + ",".join(k.__repr__() for k in self.kids) + ")"

nonterminals = [chr(ord('S')+i) for i in range(int(argv[1]))]
terminals = [chr(ord('a')+i) for i in range(int(argv[2]))]
if argv[3] == '1':
    dist = [0.25, 0.25, 0.2, 0.1, 0.1, 0.1]
elif argv[3] == '2':
    dist = [0.25, 0.25, 0.1, 0.2, 0.1, 0.1]
elif argv[3] == '3':
    dist = [0.25, 0.25, 0.1, 0.1, 0.2, 0.1]
elif argv[3] == '4':
    dist = [0.25, 0.25, 0.1, 0.1, 0.1, 0.2]
elif argv[3] == '5':
    dist = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1]

def gen_rand():
    op = choices(["N", "T", ";", "/", "*", "!"], weights=dist)[0]
    if op == "N":
        return Expr(op, choice(nonterminals))
    if op == "T":
        return Expr(op, choice(terminals))
    return Expr(op, "")

def traverse(e):
    for i in range(e.no_kids):
        e1 = gen_rand()
        e.kids[i] = traverse(e1)
    return e

for nt in nonterminals:
    print(nt + " -> ", end="")
    e = gen_rand()
    e = traverse(e)
    print(e)