L = 15
file = f'triple{L}.txt'
with open(file, 'r') as f:
    fail = 0
    succeed = [0 for _ in range(L+1)]
    for line in f:
        if ',' in line[:-1]:
            fail += 1
            continue
        s = line[:-1].index('|')
        succeed[s] += 1

print(f"Fail {fail}")
print(f"Succeed {succeed}")