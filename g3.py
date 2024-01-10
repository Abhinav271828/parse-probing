import random

def memoize(f):
  class Memo:
    def __init__(self):
      self.ncalls = 0
      self.nhits = 0
      self.memotbl = [None for _ in range(21)]
    def __repr__(self):
      #return "f: nhits: %4d / ncalls: %4d | hit ratio: %4.2f" % \
      #(self.nhits, self.ncalls, self.nhits/self.ncalls)
      return str(self.memotbl)

    def __call__(self, s):
      self.ncalls += 1
      k = len(s)
      if self.memotbl[k]:
        self.nhits += 1
        v = self.memotbl[k]
        #print(f"memoED f({k}) = {v}")
        return v
      v = f(s)
      #print(f"memoING f({k}) = {v}")
      self.memotbl[k] = v
      return v
    
    def restore(self):
      self.memotbl = [None for _ in range(21)]
  return Memo()

@memoize
def pChar(s):
  if s == '': return None
  return s[0], s[1:]

# S -> M; P
# P -> +; M; P / ε
# M -> E; T
# T -> ×; E; T / ε
# E -> V; C
# C -> ^; V; C / ε
# V -> \d / [; S; ]

@memoize
def pS(s):
  match pM(s):
    case x, s_:
      match pP(s_):
        case y, s__:
          return x+y, s__
        case y, s__, None:
          return x+y, s__, None
    case x, s_, None:
      return x, s_, None

@memoize
def pP(s):
  def alt2():
    return '', s

  match pChar(s):
    case '+', s_:
      match pM(s_):
        case x, s__:
          match pP(s__):
            case y, s___:
              return ('+' + x + y, s___)
            case y, s___, None:
              return alt2()
        case _:
          return alt2()
    case _:
      return alt2()

@memoize
def pM(s):
  match pE(s):
    case x, s_:
      match pT(s_):
        case y, s__:
          return x+y, s__
        case y, s__, None:
          return x+y, s__, None
    case x, s_, None:
      return x, s_, None

@memoize
def pT(s):
  def alt2():
    return '', s

  match pChar(s):
    case '×', s_:
      match pE(s_):
        case x, s__:
          match pT(s__):
            case y, s___:
              return ('×' + x + y, s___)
            case y, s___, None:
              return alt2()
        case x, s__, None:
          return alt2()
    case _:
      return alt2()

@memoize
def pE(s):
  match pV(s):
    case x, s_:
      match pC(s_):
        case y, s__:
          return x+y, s__
        case y, s__, None:
          return x+y, s__, None
    case x, s_, None:
      return x, s_, None

@memoize
def pC(s):
  def alt2():
    return '', s

  match pChar(s):
    case '^', s_:
      match pV(s_):
        case x, s__:
          match pC(s__):
            case y, s___:
              return ('^' + x + y, s___)
            case y, s___, None:
              return alt2()
        case x, s__, None:
          return alt2()
    case _:
      return alt2()

@memoize
def pV(s):
  match pChar(s):
    case c, s_ if c in "0123456789":
      return (c, s_)
    case '[', s_:
      match pS(s_):
        case x, s__:
          match pChar(s__):
            case ']', s___:
              return ('[' + x + ']', s___)
            case _:
              return ('[' + x, s__, None)
        case x, s__, None:
          return ('[' + x, s__, None)
    case _:
      return '', s, None

def parse(s):
  match pS(s):
    case (x, s_):
      print(f"{x}|{s_}")
      #print(f"Result: {x}; Remaining: {s_}")
    case x, s_, None:
      print(f"{x},{s_}")
      #print("Failed!")
  pS.restore()
  pP.restore()
  pM.restore()
  pT.restore()
  pE.restore()
  pC.restore()
  pV.restore()
  pChar.restore()

if __name__ == "__main__":
  alph = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '×', '^', '[', ']']
  A = len(alph)
  L = 11
  #for i in range(A**L): # This iterates over all strings
  #for i in random.sample(range(A**L), 2**20): # This randomly picks strings; almost always fails
  #  s = ''
  #  n = i
  #  for _ in range(L):
  #    s += alph[n % A]
  #    n //= A
  #  #print(s)
  #  parse(s)
  #  #print(i, s)

  for D in range(2, (L+1) // 2): # This generates only valid strings
    ds = random.choices(list(map(str,range(10))), k=D)

    B = (L - (2 * D - 1)) // 2
    for _ in range(B):
      i = random.choice(range(len(ds)))
      ds[i] = '[' + ds[i]
      i = random.choice(range(i,len(ds)))
      ds[i] = ds[i] + ']'

    os = random.choices(['+', '×', '^'], k=D-1)
    s = [ds[0]] + [y for x in zip(os, ds[1:]) for y in x]
    s = ''.join(s)
    parse(s)