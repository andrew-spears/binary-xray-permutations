"""H1 follow-up: for symmetric D, does an involution witness (pi=pi^-1) / centrosymmetric witness exist?"""
for n in range(1, 13):
    tot = inv = cen = 0
    for line in open(f'/home/claude/agents/paritydata/wit_{n}.txt'):
        p = line.split('|'); D = sorted(map(int, p[0].split())); f = int(p[4])
        if sorted(-d for d in D) != D: continue
        tot += 1; inv += f & 1; cen += f >> 1 & 1
    print(f'n={n} symmetric D={tot} with involution witness={inv} with centrosymmetric witness={cen}')
