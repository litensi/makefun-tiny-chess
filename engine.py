import json, os, sys
from urllib.request import Request, urlopen
URL = os.environ["MAKEFUN_ENV_URL"]
def post(path, body):
    req = Request(URL + path, json.dumps(body).encode(), {"content-type": "application/json"})
    return json.load(urlopen(req))
GB = [7] * 144
B = GB
SIDE = 0
CA = 0
EP = -1
HF = 0
HIST = []
HASH = 0
REPS = []
GH = []
CUR = 0
CF = ""
KS = [0, 0]
NODES = 0
STOP = 0
CAP = 120000
TT = {}
KL = [[0, 0] for _ in range(80)]
HI = [0] * 16384
VAL = [0, 100, 320, 330, 500, 900, 0, 0]
S = 0x2545F491
Z = []
for _ in range(2048):
    S ^= (S << 13) & 0xFFFFFFFF
    S ^= S >> 17
    S ^= (S << 5) & 0xFFFFFFFF
    Z.append(S & 0xFFFFFFFF)
PST = [0] * 2048
for q in range(128):
    if q & 0x88:
        continue
    f = q & 7
    r = q >> 4
    for c in (0, 1):
        rr = r if c == 0 else 7 - r
        for t in range(1, 7):
            if t == 1:
                v = rr * 8 + (10 if 2 < f < 5 else 0) + (rr * 4 if rr > 4 else 0)
            elif t < 4:
                v = 30 - 5 * abs(2 * f - 7) - 5 * abs(2 * rr - 7)
            elif t == 4:
                v = 12 * (rr == 6)
            elif t == 5:
                v = 12 - 3 * abs(2 * f - 7) - 2 * abs(2 * rr - 7)
            else:
                v = 24 if rr < 1 and 2 < f < 6 else -6 * (2 < f < 5 and 2 < rr < 6)
            PST[(q << 4) | t | (c << 3)] = v
SQ = [q for q in range(128) if not q & 0x88]
KN = (33, 31, 18, 14, -14, -18, -31, -33)
KG = (17, 16, 15, 1, -1, -15, -16, -17)
BD = (17, 15, -15, -17)
RD = (16, 1, -1, -16)
def load(fen):
    global B, GB, SIDE, CA, EP, HF, HASH, HIST, REPS, KS, CF
    CF = fen
    p = fen.split()
    GB = [7] * 144
    B = GB
    for q in range(128):
        if not q & 0x88:
            B[q] = 0
    r = 7
    f = 0
    for c in p[0]:
        if c == "/":
            r -= 1
            f = 0
        elif c.isdigit():
            f += int(c)
        else:
            B[(r << 4) | f] = " pnbrqk".index(c.lower()) + (0 if c.isupper() else 8)
            f += 1
    GB[:] = B
    SIDE = 0 if p[1] == "w" else 1
    for q in range(128):
        if not q & 0x88 and B[q] == 6:
            KS[0] = q
        elif not q & 0x88 and B[q] == 14:
            KS[1] = q
    CA = 0
    for i, c in enumerate("KQkq"):
        if c in p[2]:
            CA |= 1 << i
    EP = -1 if p[3] == "-" else ((int(p[3][1]) - 1) << 4) | "abcdefgh".index(p[3][0])
    HF = 0
    HASH = 0
    for q in range(128):
        if not q & 0x88 and B[q]:
            HASH ^= Z[(q << 4) | B[q]]
    if SIDE:
        HASH ^= 0x5A5A5A5A
    TT.clear()
    HIST = []
    REPS = GH[:] + [HASH]
def atk(sq, by):
    B = GB
    p = 1 | (by << 3)
    d = -16 if by == 0 else 16
    if B[sq + d - 1] == p or B[sq + d + 1] == p:
        return 1
    for o in KN:
        if not (sq + o) & 0x88 and B[sq + o] == p + 1:
            return 1
    for o in KG:
        if not (sq + o) & 0x88 and B[sq + o] == p + 5:
            return 1
    for ds, a, b in ((BD, 2, 4), (RD, 3, 4)):
        for o in ds:
            t = sq + o
            while not t & 0x88:
                q = B[t]
                if q:
                    if q == p + a or q == p + b:
                        return 1
                    break
                t += o
    return 0
def gen(caps, tt=0, ply=0):
    B = GB
    us = SIDE
    out = []
    pd = 16 if us == 0 else -16
    last = 7 if us == 0 else 0
    for sq in SQ:
        p = B[sq]
        if not p or p >> 3 != us:
            continue
        t = p & 7
        if t == 1:
            to = sq + pd
            if not to & 0x88 and not B[to]:
                if to >> 4 == last:
                    out += [sq << 7 | to | x << 14 for x in (5, 4, 3, 2)]
                elif not caps:
                    out.append(sq << 7 | to)
                    if (sq >> 4) == (1 if us == 0 else 6) and not B[to + pd]:
                        out.append(sq << 7 | to + pd)
            for to in (sq + pd - 1, sq + pd + 1):
                if to & 0x88:
                    continue
                q = B[to]
                if q and q >> 3 != us:
                    if to >> 4 == last:
                        out += [sq << 7 | to | x << 14 for x in (5, 4, 3, 2)]
                    else:
                        out.append(sq << 7 | to)
                elif to == EP:
                    out.append(sq << 7 | to)
        else:
            ds = KN if t == 2 else KG if t == 6 else BD if t == 3 else RD if t == 4 else BD + RD
            sl = t != 2 and t != 6
            for d in ds:
                to = sq + d
                while not to & 0x88:
                    q = B[to]
                    if q:
                        if q >> 3 != us:
                            out.append(sq << 7 | to)
                        break
                    if not caps:
                        out.append(sq << 7 | to)
                    if not sl:
                        break
                    to += d
        if t == 6 and not caps:
            if us == 0:
                if CA & 1 and not B[5] and not B[6] and not atk(4, 1) and not atk(5, 1):
                    out.append(4 << 7 | 6)
                if CA & 2 and not B[3] and not B[2] and not B[1] and not atk(4, 1) and not atk(3, 1) and not atk(2, 1):
                    out.append(4 << 7 | 2)
            else:
                if CA & 4 and not B[117] and not B[118] and not atk(116, 0) and not atk(117, 0):
                    out.append(116 << 7 | 118)
                if CA & 8 and not B[115] and not B[114] and not B[113] and not atk(116, 0) and not atk(115, 0) and not atk(114, 0):
                    out.append(116 << 7 | 114)
    caps2 = []
    quiets = []
    k = KL[ply & 63]
    for m in out:
        to = m & 0x7F
        vic = B[to]
        pr = m >> 14
        if pr or vic:
            caps2.append((VAL[vic & 7] * 9 + (pr << 8) - VAL[B[(m >> 7) & 0x7F] & 7], m))
        elif m == k[0]:
            quiets.append(m)
        else:
            quiets.append(m)
    caps2.sort(reverse=True)
    r = [m for _, m in caps2]
    if tt:
        r.insert(0, tt)
    for m in k:
        if m and m not in r and B[(m >> 7) & 0x7F] and (B[(m >> 7) & 0x7F] >> 3) == us:
            r.append(m)
    for m in out:
        if not (m >> 14) and not B[m & 0x7F] and m not in r:
            r.append(m)
    return r
def mk(m):
    global SIDE, CA, EP, HF, HASH
    B = GB
    fr = (m >> 7) & 0x7F
    to = m & 0x7F
    pc = B[fr]
    cap = B[to]
    pr = m >> 14
    us = SIDE
    pd = 16 if us == 0 else -16
    epc = -1
    if (pc & 7) == 1 and to == EP and not cap:
        epc = to - pd
    HIST.append((m, cap, epc, CA, EP, HF, HASH, 1))
    HASH ^= Z[(fr << 4) | pc] ^ Z[(to << 4) | (pr | (us << 3) if pr else pc)]
    B[fr] = 0
    B[to] = (pr | (us << 3)) if pr else pc
    if (pc & 7) == 6:
        KS[us] = to
    if epc >= 0:
        HASH ^= Z[(epc << 4) | B[epc]]
        B[epc] = 0
    elif cap:
        HASH ^= Z[(to << 4) | cap]
    if (pc & 7) == 6 and abs(to - fr) == 2:
        a = fr + 3 if to > fr else fr - 4
        b = fr + 1 if to > fr else fr - 1
        HASH ^= Z[(a << 4) | B[a]] ^ Z[(b << 4) | B[b]]
        B[b] = B[a]
        B[a] = 0
    if fr == 4:
        CA &= 12
    elif fr == 0:
        CA &= 13
    elif fr == 7:
        CA &= 14
    elif fr == 116:
        CA &= 3
    elif fr == 112:
        CA &= 7
    elif fr == 119:
        CA &= 11
    if to == 0:
        CA &= 13
    elif to == 7:
        CA &= 14
    elif to == 116:
        CA &= 3
    elif to == 112:
        CA &= 7
    elif to == 119:
        CA &= 11
    if (pc & 7) == 1 or cap:
        HF = 0
    else:
        HF += 1
    EP = (fr + to) >> 1 if (pc & 7) == 1 and abs(to - fr) == 32 else -1
    SIDE = us ^ 1
    HASH ^= 0x5A5A5A5A
    if atk(KS[us], SIDE):
        HIST[-1] = (m, cap, epc, CA, EP, HF, HASH, 0)
        un()
        return 0
    REPS.append(HASH)
    return 1
def kof(us):
    k = 6 | (us << 3)
    for q in range(128):
        if B[q] == k:
            return q
    return 0
def un():
    global SIDE, CA, EP, HF, HASH
    B = GB
    m, cap, epc, c0, e0, h0, z0, rp = HIST.pop()
    if m < 0:
        SIDE ^= 1
        CA = c0
        EP = e0
        HF = h0
        HASH = z0
        if rp:
            REPS.pop()
        return
    fr = (m >> 7) & 0x7F
    to = m & 0x7F
    pr = m >> 14
    pc = (1 | ((SIDE ^ 1) << 3)) if pr else B[to]
    B[fr] = pc
    B[to] = cap
    if (pc & 7) == 6:
        KS[SIDE ^ 1] = fr
    if epc >= 0:
        B[epc] = 1 | (SIDE << 3)
    if (pc & 7) == 6 and abs(to - fr) == 2:
        a = fr + 3 if to > fr else fr - 4
        b = fr + 1 if to > fr else fr - 1
        B[a] = B[b]
        B[b] = 0
    CA = c0
    EP = e0
    HF = h0
    HASH = z0
    SIDE = SIDE ^ 1
    if rp:
        REPS.pop()
def ev():
    B = GB
    s = 0
    wp = [0] * 8
    bp = [0] * 8
    for q in SQ:
        p = B[q]
        if p == 1:
            wp[q & 7] += 1
        elif p == 9:
            bp[q & 7] += 1
    nb = [0, 0]
    for q in SQ:
        p = B[q]
        if not p:
            continue
        if p > 14 or p == 7:
            continue
        t = p & 7
        f = q & 7
        r = q >> 4
        if t == 3:
            nb[p >> 3] += 1
        if p >> 3:
            if t == 1:
                s -= VAL[1] + PST[(q << 4) | p]
                if wp[f] == 0 and wp[f - 1 if f else 0] == 0 and wp[f + 1 if f < 7 else 7] == 0:
                    s -= 20 + 8 * (7 - r)
                if bp[f] > 1:
                    s += 10
            else:
                s -= VAL[t] + PST[(q << 4) | p]
                if t == 4 and not wp[f] and not bp[f]:
                    s -= 12
        else:
            if t == 1:
                s += VAL[1] + PST[(q << 4) | p]
                if bp[f] == 0 and bp[f - 1 if f else 0] == 0 and bp[f + 1 if f < 7 else 7] == 0:
                    s += 20 + 8 * r
                if wp[f] > 1:
                    s -= 10
            else:
                s += VAL[t] + PST[(q << 4) | p]
                if t == 4 and not wp[f] and not bp[f]:
                    s += 12
    s += nb[0] * 28 - nb[1] * 28
    return s + 10 if SIDE == 0 else 10 - s
def qs(alpha, beta, d):
    global NODES
    NODES += 1
    chk = atk(KS[SIDE], SIDE ^ 1)
    v = ev()
    if not chk:
        if v >= beta or d > 8:
            return v
        if v > alpha:
            alpha = v
    for m in gen(0 if chk else 1, 0, d):
        if not chk and v + VAL[B[m & 0x7F] & 7] + 120 < alpha:
            continue
        if not mk(m):
            continue
        s = -qs(-beta, -alpha, d + 1)
        un()
        if s >= beta:
            return s
        if s > alpha:
            alpha = s
    if chk and alpha == -30000:
        return -30000 + d
    return alpha
def ng(d, alpha, beta, ply):
    global NODES, STOP, HASH, EP, SIDE, CA, HF, REPS
    NODES += 1
    if NODES > CAP or STOP:
        STOP = 1
        return 0
    if ply and REPS and HASH != REPS[-1] and HASH in REPS:
        return -4
    tt = TT.get(HASH)
    if tt and tt[0] >= d:
        sv = tt[2]
        if sv > 29000:
            sv -= ply
        elif sv < -29000:
            sv += ply
        if tt[1] == 0:
            return sv
        if tt[1] == 1 and sv >= beta:
            return sv
        if tt[1] == 2 and sv <= alpha:
            return sv
    if d < 1:
        return qs(alpha, beta, 0)
    chk = atk(KS[SIDE], SIDE ^ 1)
    if not chk:
        v = ev()
        if v >= beta:
            return v
        if v > alpha:
            alpha = v
        if d > 2 and beta - alpha < 200:
            HIST.append((-1, 0, -1, CA, EP, HF, HASH, 1))
            EP = -1
            SIDE ^= 1
            HASH ^= 0x5A5A5A5A
            REPS.append(HASH)
            s = -ng(d - 3, -beta, -beta + 1, ply + 1)
            un()
            if STOP:
                return 0
            if s >= beta:
                return beta
    best = -30000
    bm = 0
    n = 0
    a0 = alpha
    for m in gen(0, tt[3] if tt else 0, ply):
        to = m & 0x7F
        quiet = not (m >> 14) and not B[to]
        if not mk(m):
            continue
        n += 1
        ex = 1 if atk(KS[SIDE], SIDE ^ 1) else 0
        if quiet and n > 3 and d > 2 and not chk:
            s = -ng(d - 2 + ex, -alpha - 1, -alpha, ply + 1)
            if not STOP and s > alpha:
                s = -ng(d - 1 + ex, -beta, -alpha, ply + 1)
        elif n > 1:
            s = -ng(d - 1 + ex, -alpha - 1, -alpha, ply + 1)
            if not STOP and s > alpha and s < beta:
                s = -ng(d - 1 + ex, -beta, -alpha, ply + 1)
        else:
            s = -ng(d - 1 + ex, -beta, -alpha, ply + 1)
        un()
        if STOP:
            return 0
        if s > best:
            best = s
            bm = m
            if s > alpha:
                alpha = s
                if alpha >= beta:
                    if quiet:
                        HI[((m >> 7) & 0x7F) << 7 | to] += d * d
                        if m != KL[0][0]:
                            KL[0][1] = KL[0][0]
                            KL[0][0] = m
                    break
    if not n:
        return -30000 + ply if chk else 0
    sv = best + ply if best > 29000 else best - ply if best < -29000 else best
    TT[HASH] = (d, 1 if best >= beta else 2 if best <= a0 else 0, sv, bm)
    return best
def go():
    global NODES, STOP
    load(CF)
    SP = GB[:]
    for x in KL:
        x[0] = 0
        x[1] = 0
    RT = []
    for m in gen(0):
        Bx = GB[(m >> 7) & 0x7F]
        if (not Bx or (Bx >> 3) != SIDE) and not (m >> 14):
            continue
        if mk(m):
            RT.append(m)
            un()
    if not RT:
        RT = gen(0)[:1]
    best = RT[0]
    for d in range(1, 13):
        NODES = 0
        STOP = 0
        alpha = -30000
        loc = best
        first = 1
        for m in RT:
            if not mk(m):
                continue
            if first:
                s = -ng(d - 1, -30000, 30000, 1)
                first = 0
            else:
                s = -ng(d - 1, -alpha - 1, -alpha, 1)
                if not STOP and s > alpha:
                    s = -ng(d - 1, -30000, -alpha, 1)
            if HASH in REPS[:-2]:
                s -= 6
            un()
            if STOP:
                break
            if s > alpha:
                alpha = s
                loc = m
        if not STOP:
            best = loc
            RT.remove(best)
            RT.insert(0, best)
        if NODES > CAP // 2:
            break
    GB[:] = SP
    HIST.clear()
    fr = (best >> 7) & 0x7F
    to = best & 0x7F
    pr = best >> 14
    f = "abcdefgh"
    return f[fr & 7] + str((fr >> 4) + 1) + f[to & 7] + str((to >> 4) + 1) + (" pnbrqk"[pr] if pr else "")
def main():
    global CUR
    while 1:
        g = post("/game", {})
        if g["status"] == "done":
            break
        if g["game"] != CUR:
            CUR = g["game"]
            GH.clear()
        while g["status"] == "your_move":
            load(g["fen"])
            GH.append(HASH)
            m = go()
            if m not in g["legal_moves"]:
                print("illegal", m, file=sys.stderr)
                m = g["legal_moves"][0]
            g = post("/move", {"game": g["game"], "move": m})
        print(g.get("outcome"), g.get("reason"), file=sys.stderr)
main()
