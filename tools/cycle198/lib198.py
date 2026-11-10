"""Cycle 198 helpers (Python, independent of cmp198.c): 2-cores of crib graphs, one-wrong-letter decoding via lib197."""
from lib197 import *
def edges_of(rec, model, m, n, drop=()):
    kp, kc, cv = rec; pos = kp if model in "PD" else kc
    return {t: (pos[t] % m, m + pos[t] % n) for t in range(24) if cv[t] >= 0 and t not in drop}
def core(E):
    E = dict(E)
    while True:
        deg = {}
        for (u, v) in E.values(): deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
        leaf = [t for t, (u, v) in E.items() if deg[u] == 1 or deg[v] == 1]
        if not leaf: return frozenset(E)
        for t in leaf: E.pop(t, None)
def drop_slot(rec, slots):
    kp, kc, cv = rec; cv = list(cv)
    for s in slots: cv[s] = -1
    return [kp, kc, cv]
def equivalent_slots(rec, model, m, n, slot):
    """all slots t whose deletion gives the same 2-core as deleting slot (the same one-error event)."""
    E = edges_of(rec, model, m, n); c = core({t: e for t, e in E.items() if t != slot})
    return [t for t in E if core({u: e for u, e in E.items() if u != t}) == c]
