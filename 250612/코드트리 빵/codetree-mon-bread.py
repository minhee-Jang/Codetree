from collections import deque
D = [(-1, 0), (0, -1), (0, 1), (1, 0)] # 상 좌 우 하 우선순위

def inrange(r, c):
    return 0<=r<N and 0<=c<N

def FindBase(er, ec, cant, p):  # occupy 상관없음 -> 순간이동할거임
    global now, occupy
    # 행, 열이 작은 순서대로 고르기
    q = deque([(er, ec)])
    v = [[False for _ in range(N)] for _ in range(N)]
    tmp = [[N**2 for _ in range(N)] for _ in range(N)]
    tmp[er][ec] = 0
    v[er][ec] = True
    minDist = (N*N, N+1, N+1)

    while q:
        r, c = q.popleft()
        for dr, dc in D:
            nr, nc = r + dr, c + dc

            if inrange(nr, nc) and not v[nr][nc] and not occupy[nr][nc]: # 방문 안한 곳
                tmp[nr][nc] = min(tmp[nr][nc], tmp[r][c] + 1)
                v[nr][nc] = True
                q.append((nr, nc))

                if game[nr][nc] == 1:
                    tmpDist = (tmp[nr][nc], nr, nc)
                    if minDist > tmpDist: # 최단거리
                        minDist = tmpDist # 업데이트

    now[p] = (minDist[1], minDist[2]) # 좌표 업뎃
    cant.append((minDist[1], minDist[2]))
    return cant

def Go(turn, cant):
    global now, Done

    for i in range(1, turn+1): #움직일 대상.
        if visited[i]: continue
        q = deque([(now[i][0], now[i][1], [])])  # 현재 위치/ 이동 경로
        v = [[False for _ in range(N)] for _ in range(N)]
        v[now[i][0]][now[i][1]] = True 
        flag = True

        while flag:
            r, c, route = q.popleft()
            for dr, dc in D:  
                nr, nc = r + dr, c + dc
                if not inrange(nr, nc): continue
                if v[nr][nc] == True: continue
                if occupy[nr][nc] == True: continue
                # 방문 가능
                if nr == want[i][0] and nc == want[i][1]: # 편의점 도착
                    route.append((r, c))

                    if len(route) == 1:
                        cant.append((nr, nc))
                        visited[i] = True
                        now[i] = (nr, nc)
                        Done.append(i)
                        flag = False
                        break
                    else:
                        route.append((r, c))
                        now[i] = route[1]  
                        flag = False
                        break
                else:
                    test = route[:]
                    test.append((r, c))
                    q.append((nr, nc, test))
                    v[nr][nc] = True

    return cant

if __name__=="__main__":

    N, M = map(int, input().split())

    game = []
    occupy = [[False for _ in range(N)] for _ in range(N)]
    for _ in range(N):
        t = list(map(int, input().split()))
        game.append(t)

    want = {i:(0,0) for i in range(1, M+1)} # 편의점 정답
    now = {i:(0,0) for i in range(1, M+1)} # 지금 위치
    visited = {i: False for i in range(1, M+1)} # 방문 여부

    
    for i in range(1, M+1):
        r, c = map(int, input().split())
        want[i] = (r-1, c-1)
        game[r-1][c-1] = 2

    ############################################################
    Done = []
    minute = 0  
    while len(Done) != M: # 모두가 완료할때까지
        minute += 1
        cant = []
        if minute ==1:
            er, ec = want[minute]
            cant = FindBase(er, ec, cant, minute)
            for a, b in cant:
                occupy[a][b] = True
        else:
            if minute<=M:  # T는 베이스캠프 탐색
                # 편의점을 향해 이동 -> 현재가 T분이라면 1 ~ T-1 사람만 탐색 (N*N*M
                cant = Go(minute-1, cant)
                for a, b in cant:
                    occupy[a][b] = True
                # 베이스캠프 찾기
                er, ec = want[minute]
                cant = FindBase(er, ec, cant, minute)  # 현재 위치
                for a, b in cant:
                    occupy[a][b] = True
            else:
                cant = Go(M, cant)
                # 이동 불가한 칸 체크  -> cant
                for a, b in cant:
                    occupy[a][b] = True

    print(minute)