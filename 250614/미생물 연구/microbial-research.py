from collections import deque
D = [(0, 1), (1, 0), (-1, 0), (0, -1)]

def in_range(r,c):
    return 0<=r<N and 0<=c<N

def minmax(route):
    minr, minc, maxr, maxc = N*N, N*N, -1, -1
    for r, c in route:
        minr = min(minr, r)
        minc = min(minc, c)
        maxr = max(maxr, r)
        maxc = max(maxc, c)

    return minr, minc, maxr, maxc

def moveMicro(prior, loc, t):
    global alive

    newEx = [[0 for _ in range(N)] for _ in range(N)]  # 새로운 배양용기
    # 살아있는 애들로만 배양용기 이동 -> 새로운 배양용기
    put = {i:False for i in range(1, Q+1)}

    n=0
    while n<len(prior):

        if not alive[prior[n][1]]: continue
        minr, minc, maxr, maxc = minmax(prior[n][2]) # 최대최소
        dr, dc = maxr - minr, maxc - minc
        for c in range(N): # c가 작을수록

             if put[prior[n][1]] == True: break
             for r in range(N): # r이 작을수록
                possible = True
                if newEx[r][c] != 0:
                    continue
                if in_range(r+dr, c+dc):
                    # 검사하고 붙이기  ###########
                    for i in range(r, r+dr+1):
                        for j in range(c, c+dc+1): #
                            if newEx[i][j] != 0:
                                possible = False
                                break
                        if not possible: break
                    # 좌표 계산
                    if possible:

                        put[prior[n][1]] = True
                        br, bc = r - minr, c - minc
                        newR = []
                        for a, b in loc[prior[n][1]][2]:
                            nbr, nbc = a + br, b + bc # 블럭 위치
                            newEx[nbr][nbc] = prior[n][1]
                            newR.append((nbr, nbc))
                        loc[prior[n][1]][2] = newR # 좌표 교체
                        break
        n+=1

    for n in range(len(prior)):  # 죽은애들
        if not put[prior[n][1]]:
            alive[prior[n][1]] = False
            loc[prior[n][1]][2] = []

    return newEx, loc

def result(ex):
    global loc

    ans = 0
    q = deque([(0,0)])
    visited = [[False for _ in range(N)] for _ in range(N)]
    meet = []

    while q:
        r, c = q.popleft()
        for dr, dc in D:
            nr, nc = r + dr, c + dc
            if in_range(nr, nc) and not visited[nr][nc]:
                q.append((nr, nc))
                visited[nr][nc] = True
                if ex[r][c] != ex[nr][nc] and ex[r][c] !=0 and ex[nr][nc] != 0: # 둘이 다른 종이
                    if (ex[r][c], ex[nr][nc]) not in meet and (ex[nr][nc], ex[r][c]) not in meet:
                        meet.append((ex[r][c], ex[nr][nc]))

    for a, b in meet:
        ans += loc[a][0]*loc[b][0]

    print(ans)
    return

def putMicro(ex, micro, n, loc):  # 배양용기는 moveMicro에서 시작됨
    global alive

    r1, c1, r2, c2 = micro
    for i in range(r1, r2+1):
        for j in range(c1, c2+1):
            ex[i][j] = n # 현재 미생물

    visited = [[False for _ in range(N)] for _ in range(N)]
    find = {i:False for i in range(1, n+1)}
    kill = []

    for i in range(N):
        for j in range(N):
            m = ex[i][j]
            if m>0 and not visited[i][j]:
                cnt = 1

                if not find[m]:
                    loc[m][2] = []
                if find[m] and m not in kill: # 이미 찾음 (두 무리로 나눠지게 될 경우 -> 모두 사라짐)
                    kill.append(m) # 나중에 죽이기 (좌표는 모두 기록)
                find[m] = True

                q = deque([(i, j)])
                visited[i][j] = True
                loc[m][2].append((i, j))
                #route = [(i, j)]
                while q: # BFS
                    r, c = q.popleft()
                    for dr, dc in D:
                        nr, nc = r+dr, c+dc
                        if (in_range(nr, nc) and not visited[nr][nc]) and ex[nr][nc] == m:
                            q.append((nr, nc))
                            visited[nr][nc] = True
                            loc[m][2].append((nr, nc))
                            cnt +=1
                loc[m][0] = cnt
    # Loc 업데이트, Kill 진행

    for i in kill:
        for kr, kc in loc[i][2]:
            ex[kr][kc] = 0
        alive[i] = False
        loc[i][2] = []

    for i in range(n):
        if not find[i+1]:
            alive[i] = False
            loc[i+1][2] = []

    return ex, loc

if __name__=="__main__":

    N, Q = map(int, input().split())
    micro = [(0,0)]
    for _ in range(Q):
        c1, r1, c2, r2 = map(int, input().split())
        micro.append((r1, c1, r2-1, c2-1))  # 위로 뒤집어서 보게 -> 좌측 상단으로

    loc = {i:[0, i, []] for i in range(1, Q+1)} # 넓이, 투입순서, 현재 위치
    alive = {i:True for i in range(1, Q+1)} # 생존 여부
    ex = [[0 for _ in range(N)] for _ in range(N)]  # 배양용기

    for i in range(1, Q+1): # 새로운거 심기 -> 이동 (미생물 수만큼)
        ex, loc = putMicro(ex, micro[i], i, loc)

        tmp = []
        for j in range(1, i+1):
            if alive[j]:
                tmp.append(loc[j])
        prior = sorted(tmp, key=lambda x: (-x[0],x[1]))
        ex, loc = moveMicro(prior, loc, i)

        result(ex)


