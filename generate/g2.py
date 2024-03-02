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

# S -> [; T; ]
# T -> A; b / a; B / a; S; b
# A -> a; A / ε
# B -> b; B / ε

@memoize
def pChar(s):
  if s == '': return None
  return s[0], s[1:]

@memoize
def pS(s):
  match pChar(s):
    case '[', s_:
        match pT(s_):
          case x, s__:
            match pChar(s__):
              case ']', s___:
                return ('[' + x + ']', s___)
              case _:
                return ('[' + x, s__, None)
          case x, s__, None:
            return '[' + x, s__, None
    case _:
      return '', s, None

@memoize
def pT(s):

  def alt3():
    match pChar(s):
      case 'a', s_:
        match pS(s_):
          case x, s__:
            match pChar(s__):
              case 'b', s___:
                return ('a' + x + 'b', s___)
              case _:
                return ('a' + x, s__, None)
          case x, s__, None:
            return 'a' + x, s__, None
      case _:
        return '', s, None

  def alt2():
    match pChar(s):
      case 'a', s_:
        match pB(s_):
          case y, s__:
            return ('a' + y, s__)
          case _:
            return alt3()
      case _:
        return alt3()

  match pA(s):
    case x, s_:
        match pChar(s_):
          case 'b', s__:
            return (x + 'b', s__)
          case _:
            return alt2()
    case _:
      return alt2()

@memoize
def pA(s):
  def alt2():
    return ('', s)
  match pChar(s):
    case 'a', s_:
        match pA(s_):
          case x, s__:
            return ('a'+x, s__)
          case _:
            return alt2()
    case _:
      return alt2()

@memoize
def pB(s):
  def alt2():
    return ('', s)
  match pChar(s):
    case 'b', s_:
        match pB(s_):
          case x, s__:
            return ('b'+x, s__)
          case _:
            return alt2()
    case _:
      return alt2()

def parse(s):
  match pS(s):
    case (x, s_):
      print(f"{x}|{s_}")
      #print(f"Result: {x}; Remaining: {s_}")
    case x, s_, None:
      print(f"{x},{s_}")
      #print("Failed!")
  pS.restore()
  pT.restore()
  pA.restore()
  pB.restore()
  pChar.restore()

if __name__ == "__main__":
  alph = ['a', 'b', '[', ']']
  A = len(alph)
  L = 20
  for i in range(A**L): # This iterates over all strings
  #for i in random.sample(range(A**L), 2**20): # This randomly picks strings
    s = ''
    n = i
    for _ in range(L):
      s += alph[n % A]
      n //= A
    #print(s)
    parse(s)
    #print(i, s)