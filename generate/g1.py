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

# S -> A; B
# A -> a; A / ε
# B -> b; B / ε

@memoize
def pChar(s):
  if s == '': return None
  return s[0], s[1:]

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

@memoize
def pS(s):
  match pA(s):
    case x, s_:
      match pB(s_):
        case y, s__:
          return (x+y, s__)
        case _:
          return x, s_, None
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
  pA.restore()
  pB.restore()
  pChar.restore()

if __name__ == "__main__":
  alph = ['a', 'b']
  A = len(alph)
  L = 20
  for i in range(2**L):
    s = ''
    n = i
    for _ in range(L):
      s += alph[n % A]
      n //= A
    #print(s)
    parse(s)
    #print(i, s)