"""Parse Conway's 92-element table (Wikipedia 'Look-and-say sequence', raw wikitext, fetched 2026-11-25) -> {string: (Z, symbol)} and decay lists."""
import re
def load(fn='las_wiki.txt'):
    L = open(fn).read().split('\n')
    i0 = next(i for i, l in enumerate(L) if 'All "atomic elements"' in l)
    i1 = next(i for i, l in enumerate(L) if 'Transuranic elements' in l)
    cells = [l[1:].strip() for l in L[i0:i1] if l.startswith('|') and not l.startswith('|-') and not l.startswith('|}')]
    T = {}
    k = 0
    while k + 5 <= len(cells):
        if cells[k].isdigit() and re.fullmatch(r'[123]+', cells[k + 2]):
            T[cells[k + 2]] = (int(cells[k]), cells[k + 1], cells[k + 3].split('.')); k += 5
        else: k += 1
    return T
if __name__ == '__main__':
    T = load(); print(len(T), sorted(v[0] for v in T.values()) == list(range(1, 93)))
