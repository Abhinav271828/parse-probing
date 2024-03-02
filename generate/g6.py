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

# S -> A / B / C / ε
# A -> [; S; ]; S
# B -> (; S; ); S
# C -> {; S; }; S

@memoize
def pS(s):
  def alt2():
    return '', s
  
  match pA(s):
    case x, s_:
      return x, s_
    case _:
      match pB(s):
        case x, s_:
          return x, s_
        case _:
          match pC(s):
            case x, s_:
              return x, s_
            case _:
              return alt2()

@memoize
def pA(s):
  match pChar(s):
    case '[', s_:
      match pS(s_):
        case x, s__:
          match pChar(s__):
            case ']', s___:
              match pS(s___):
                case y, s____:
                  return ('[' + x + ']' + y, s____)
                case y, s____, None:
                  return y, s____, None
            case _:
              return '[' + x, s__, None
        case x, s__, None:
          return '[' + x, s__, None
    case _:
      return '', s, None

@memoize
def pB(s):
  match pChar(s):
    case '(', s_:
      match pS(s_):
        case x, s__:
          match pChar(s__):
            case ')', s___:
              match pS(s___):
                case y, s____:
                  return ('(' + x + ')' + y, s____)
                case y, s____, None:
                  return y, s____, None
            case _:
              return '(' + x, s__, None
        case x, s__, None:
          return '(' + x, s__, None
    case _:
      return '', s, None

@memoize
def pC(s):
  match pChar(s):
    case '{', s_:
      match pS(s_):
        case x, s__:
          match pChar(s__):
            case '}', s___:
              match pS(s___):
                case y, s____:
                  return ('{' + x + '}' + y, s____)
                case y, s____, None:
                  return y, s____, None
            case _:
              return '{' + x, s__, None
        case x, s__, None:
          return '{' + x, s__, None
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
  pC.restore()
  pChar.restore()

if __name__ == "__main__":
  alph = ['[', ']', '(', ')', '{', '}']
  A = len(alph)
  L = 20
  #for i in range(A**L): # This iterates over all strings
  #for i in random.sample(range(A**L), 2**20): # This randomly picks strings
  #  s = ''
  #  n = i
  #  for _ in range(L):
  #    s += alph[n % A]
  #    n //= A
  #  parse(s)

  op = ['[', '(', '{']
  cl = [']', ')', '}']
  def gen_dyck3(l):
    if l == 0: return ''
    btype = random.choice([0, 1, 2])
    prod = random.choice([0, 1])
    match prod:
      case 0:
        return (op[btype] + gen_dyck3(l-2) + cl[btype])
      case 1:
        try: l_ = random.choice(range((l-2) // 2))
        except IndexError: l_ = 0
        return (op[btype] + gen_dyck3(l_ * 2) + cl[btype] + gen_dyck3(l - (2* l_) - 2))
  
  for _ in range(2**20): # This generates only valid strings
    s = gen_dyck3(L)
    parse(s)