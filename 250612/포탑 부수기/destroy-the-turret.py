from collections import deque
D = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 우 하 좌 상
D8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # 폭탄방향
def inrange(r, c):
    if 0<=r<N and 0<=c<M:
        return r, c
    else:
        if r<0:
            r = N -1
        elif r>=N:
            r = 0
        if c<0:
            c = M -1
        elif c>=M:
            c = 0
        return r, c


def pickAttacker(score, att): # 점수판, attack 이력
    # 공격력 가장 낮은 포탑 (공격자) / 공격력 가장 높은 포탑 (대상자)
    minAtt = (50000, 0, 0, 0)   # 공격력 낮은 / 최신 공격/ r+c 큰/ c가 큰
    maxAtt = (0, 0, 0, 0)   # 공격력 높은/ 가장 오래된 공격/ r+c가 작은/ c가 작은
    attacker = (0, 0)
    toWhere = (0, 0)

    for r in range(N):
        for c in range(M):
            if score[r][c] !=0: # 부서진 포탑 x
                turn = (score[r][c], att[r][c], -(r+c), -c)
                if minAtt > turn: # 공격자 업데이트
                    minAtt = turn
                    attacker = (r, c)

                if maxAtt < turn:
                    maxAtt = turn  #
                    toWhere = (r, c)
    return attacker, toWhere

def RaiserAtt(topScore, start, end):
    group = [start, end]
    q = deque([(start[0], start[1], [])])
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[start[0]][start[1]] = True
    point = topScore[start[0]][start[1]]
    halfp = point//2

    while q:
        r, c, route = q.popleft()
        for dr, dc in D:
            nr, nc = inrange(r+dr, c+dc)
            if topScore[nr][nc] ==0: continue
            if visited[nr][nc]: continue

            if nr == end[0] and nc == end[1]:
                topScore[nr][nc] -= point
                for br, bc in route:
                    topScore[br][bc] -= halfp
                    group.append((br, bc))
                return topScore, True, group

            else:
                test = route[:]
                test.append((nr, nc))
                visited[nr][nc] = True
                q.append((nr, nc, test))

    return topScore, False, group

def BombAtt(topScore, start, end):
    group = [start, end]
    (r, c) = end
    point = topScore[start[0]][start[1]]
    topScore[end[0]][end[1]] -= point
    halfp = point // 2

    for dr, dc in D8:
        nr, nc = inrange(r + dr, c + dc)
        if (nr, nc) == start: continue
        if topScore[nr][nc] == 0: continue

        topScore[nr][nc] -= halfp
        group.append((nr, nc))

    return topScore, group

if __name__=="__main__":

    N, M, K = map(int, input().split())  # N이 행, M이 열

    topScore = []
    attack = [[0 for _ in range(M)] for _ in range(N)]
    haveAttack = []

    top = 0
    for _ in range(N):
        t = list(map(int, input().split()))
        topScore.append(t)
        zero = t.count(0)
        top += (M - zero)


    for i in range(K):
        cnt = 0
        fromAtt, to = pickAttacker(topScore, attack)
        attack[fromAtt[0]][fromAtt[1]] = -(i+1)
        topScore[fromAtt[0]][fromAtt[1]] += (N + M)
        topScore, find, group = RaiserAtt(topScore, fromAtt, to)

        if not find:
            # 포탄 던지기 공격
            topScore, group = BombAtt(topScore, fromAtt, to)

        for a in range(N):
            for b in range(M):
                # 부서짐
                if topScore[a][b] <=0:
                    topScore[a][b] = 0
                    cnt += 1
                # 포탑 정비
                if (a, b) not in group:
                    if topScore[a][b] >0 : #부서지지 않은 포탑 중 공격과 무관
                        topScore[a][b] += 1
        if N*M - cnt == 1:
            break

    # answer
    ans = max([max(row) for row in topScore])
    print(ans)