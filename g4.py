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

# S -> &(A; c); a; K; B
# K -> a; K / ε
# A -> a; A?; b
# B -> b; B?; c

@memoize
def pS(s):
  match pA(s):
    case x, s_:
      match pChar(s_):
        case 'c', s__:
          match pChar(s):
            case 'a', s_:
              match pK(s_):
                case x, s__:
                  match pB(s__):
                    case y, s___:
                      return ('a' + x + y, s___)
                    case y, s___, None:
                      return ('a' + x + y, s___)
                case x, s__, None:
                    return ('a' + x, s__)
            case _:
              return '', s, None
        case _:
          return '', s, None
    case _:
      return '', s, None

@memoize
def pK(s):
  match pChar(s):
    case 'a', s_:
      match pK(s_):
        case x, s__:
          return ('a' + x, s__)
        case _:
          return 'a', s
    case _:
      return '', s

@memoize
def pA(s):
  match pChar(s):
    case 'a', s_:
      match pA(s_):
        case x, s__:
          match pChar(s__):
            case 'b', s___:
              return ('a' + x + 'b', s___)
            case _:
              return ('a' + x, s__, None)
        case _:
          match pChar(s_):
            case 'b', s__:
              return ('a' + 'b', s__)
            case _:
              return ('a', s_, None)
    case _:
      return '', s, None

@memoize
def pB(s):
  match pChar(s):
    case 'b', s_:
      match pB(s_):
        case x, s__:
          match pChar(s__):
            case 'c', s___:
              return ('b' + x + 'c', s___)
            case _:
              return ('b' + x, s__, None)
        case _:
          match pChar(s_):
            case 'c', s__:
              return ('b' + 'c', s__)
            case _:
              return ('b', s_, None)
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
  pK.restore()
  pA.restore()
  pB.restore()
  pChar.restore()

if __name__ == "__main__":
  alph = ['a', 'b', 'c']
  A = len(alph)
  L = 12
  for i in range(A**L): # This iterates over all strings
  #for i in random.sample(range(A**L), 2**20): # This randomly picks strings; almost always fails
    s = ''
    n = i
    for _ in range(L):
      s += alph[n % A]
      n //= A
    #print(s)
    parse(s)
    #print(i, s)