from collections import deque
D8 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]  # 시계 방향

def myprint(arr):
    for lst in arr:
        print(*lst)
    print()

def CalDist(r1 ,c1, r2, c2):
    return abs(r1- r2) + abs(c1 - c2)

def in_range(r, c):
    return 0<=r<N and 0<=c<N

def findRoute(sr, sc, er, ec):
    q = deque([(sr, sc)])
    v = [[0]*N for _ in range(N)] # 어디서 왔는지. 직전 위치를 저장
    v[sr][sc] = (sr, sc)

    while q:
        r, c = q.popleft()
        if r == er and c == ec: # 목적지
            route = []
            cr, cc = v[r][c]
            while (cr, cc) != (sr, sc):
                route.append((cr, cc))
                cr, cc = v[cr][cc] # 계속 역추적
            return route[::-1]  # 역순
        # 네 방향
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)): # 상하좌우
            nr, nc = r + dr, c + dc
            if in_range(nr, nc) and v[nr][nc]==0 and arr[nr][nc]==0: # 도로, 아직 안간 곳, 범위 내
                q.append((nr, nc))
                v[nr][nc] = (r, c)

    return -1

def mark_line(v, ci, cj, dr):
    while in_range(ci, cj):
        v[ci][cj] = 2 # 전사에 가려짐
        ci, cj = ci + D8[dr][0], cj + D8[dr][1]

def mark_safe(v, si, sj, dr, orgD):
    # 직진
    ci, cj = si + D8[dr][0], sj + D8[dr][1]
    mark_line(v, ci, cj, dr)

    ci, cj = si + D8[orgD][0], sj + D8[orgD][1]
    while in_range(ci, cj):
        mark_line(v, ci, cj, dr)
        ci, cj = ci + D8[orgD][0], cj + D8[orgD][1]


def make_stone(marr, mi, mj, dr):
    # dr 방향으로 >0 만날때까지 1 표시, 이후 2
    v = [[0 for _ in range(N)] for _ in range(N)]
    cnt = 0

    ni, nj = mi + D8[dr][0], mj + D8[dr][1]
    while in_range(ni, nj):
        v[ni][nj] = 1
        if marr[ni][nj] > 0:
            cnt += marr[ni][nj]
            ni, nj = ni + D8[dr][0], nj + D8[dr][1]
            mark_line(v, ni, nj, dr)
            break
        ni, nj = ni + D8[dr][0], nj + D8[dr][1]

    # dr -1, dr  +1 방향으로 동일처리 -> 대각선 원점으로 dr 방향
    for orgD in ((dr -1)%8, (dr + 1)%8):
        si, sj = mi + D8[orgD][0], mj + D8[orgD][1]
        while in_range(si, sj): # 대각선 처리
            if v[si][sj] ==0 and marr[si][sj]>0: # 원점 좌표 검사
                v[si][sj] = 1
                cnt += marr[si][sj]
                mark_safe(v, si, sj, dr, orgD)
                break # 만나면 끝

            # 안만남
            ci, cj = si, sj
            while in_range(ci, cj):   #직진 처리
                if v[ci][cj] ==0:
                    v[ci][cj] = 1 # 시야처리
                    if marr[ci][cj]>0:
                        cnt += marr[ci][cj]
                        mark_safe(v, ci, cj, dr, orgD)
                        break
                else: # 이미 가본 곳
                    break
                ci, cj = ci + D8[dr][0], cj + D8[dr][1] # 직진 처리 방향
            si, sj = si + D8[orgD][0], sj + D8[orgD][1] # 대각선 처리 방향

    return v, cnt

def move_men(v, mi, mj):
    # 상하좌우/ 좌우상하 -> 메두사 시야가 아니면
    move, att = 0, 0

    for dirs in (((-1, 0), (1, 0), (0, -1), (0, 1)), ((0, -1), (0, 1), (-1, 0), (1, 0))):
        for id in range(len(men)-1, -1, -1):
            ci, cj = men[id]
            if v[ci][cj] == 1: continue # 돌

            dist = CalDist(mi, mj, ci, cj) # 현재거리
            for di, dj in dirs:
                ni, nj = ci + di, cj + dj
                # 메두사 시야 아니고, 메두사랑 가까워지는 방향
                if in_range(ni, nj) and v[ni][nj] != 1 and dist>CalDist(ni, nj, mi, mj):
                    if (ni, nj) == (mi, mj):
                        att +=1
                        men.pop(id)
                    else:
                        men[id] = (ni, nj)
                    move +=1
                    break

    return move, att

if __name__=='__main__':
    N, M  = map(int, input().split())
    sr, sc, er, ec = map(int, input().split())
    tmp = list(map(int, input().split()))

    men = []
    for i in range(0, M*2, 2):
        men.append((tmp[i], tmp[i+1]))

    arr = []
    for _ in range(N):
        t = list(map(int, input().split()))
        arr.append(t)

    v = [[0] * N for _ in range(N)]

    route = findRoute(sr, sc, er, ec)
    if route==-1:
        print(-1)
    else:
        for mi, mj in route: # 메두사의 최소 경로 따라
            moveCnt, attackCnt = 0, 0

            # 메두사 이동 -> 최단거리 한칸 (전사마주치면 삭제)
            for i in range(len(men)-1, -1, -1): # 삭제 역순이 더 빠름
                if men[i] == (mi, mj): # 메두사
                    men.pop(i)
            # 메두사의 시선 -> 상하좌우 네방향
            # v : 메두사 시선 1, 전사에 가려진 곳 2, 빈 땅 0 (시선처리)
            marr = [[0]*N for _ in range(N)] # 전사 수 표시
            for ti, tj in men:
                marr[ti][tj] += 1

            maxStone = -1
            v = []
            for dr in (0, 4, 6, 2):
                tv, tstone = make_stone(marr, mi, mj, dr)
                if maxStone < tstone:
                    maxStone = tstone
                    v = tv

            # 전사들의 이동: 메두사 있는 경우
            moveCnt, attackCnt = move_men(v, mi, mj)
            print(moveCnt, maxStone, attackCnt)
        print(0)
    # 도착하면 0 출력, 프로그램 종료
