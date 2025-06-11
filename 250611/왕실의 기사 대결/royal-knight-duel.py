D = [(-1, 0), (0, 1), (1, 0), (0, -1)]
def inrange(r, c):
    return 0 <= r < L and 0 <= c < L

def moveKnight(knight, locKnight, k, d):
    global chess, physical
    # 밀려나면 연쇄적으로 밀려나야함 -> 이동하려는 방향의 끝에 벽 : 몯 이동할 수 벗음
    newKnight = [[0 for _ in range(L)] for _ in range(L)] # 복사하려고 하는 판
    newlocKnight = {i: [] for i in range(1, N + 1)}  # knight 좌표
    stack = [k] # 밀쳐질 기사
    noDam = []
    visited = [False for _ in range(N+1)]

    while stack:
        ki = stack.pop()
        visited[ki] = True
        if physical[ki]>0 : # 살아있는 기사
            for r, c in locKnight[ki]: # 좌표 값
                nr, nc = r + D[d][0], c + D[d][1]  # 이동방향
                if inrange(nr, nc) and chess[nr][nc] != 2: # 이동 가능
                    newlocKnight[ki].append((nr, nc))
                    newKnight[nr][nc] = ki
                    if (knight[nr][nc] != ki and knight[nr][nc] > 0):
                        if not visited[knight[nr][nc]]: # 다른 기사 만남.
                            stack.append(knight[nr][nc])
                            visited[knight[nr][nc]] = True
                else:
                    return knight, locKnight, noDam, False # Damge 계산 x

    for i in range(1, N+1):
        if len(newlocKnight[i]) == 0 and physical[i]>0: # 밀리지 않음
            newlocKnight[i] = locKnight[i]
            for r, c in newlocKnight[i]:
                newKnight[r][c] = i
            noDam.append(i)
    return  newKnight, newlocKnight, noDam, True # Damge 계산

def damage(locKnight, knight, ans, k, no):  # 위치 계산 / 죽으면 좌표 없애
    global chess, physical

    for i in range(1, N+1):
        dam = 0
        if i!=k and i not in no:  # 명령 받은 기사 제외 / 움직이지 않은 기사 제외

            if physical[i]>0:
                for r, c in locKnight[i]:
                    if chess[r][c] == 1: # 함정
                        dam += 1
            ans[i] += dam
            if physical[i] - dam <=0: # 죽었으면 knight에서 삭제
                physical[i] = 0
                for r, c in locKnight[i]:
                    knight[r][c] = 0 # 삭제

    return ans, knight

if __name__=="__main__":
    # L 체스판 40 / N 기사 수 30
    L, N, Q = map(int, input().split())
    chess = []  # 0 ~ L-1 index
    for _ in range(L):
        t = list(map(int, input().split()))
        chess.append(t)

    knight = [[0 for _ in range(L)] for _ in range(L)]
    physical = {i:0 for i in range(1, N+1)}   # 체력 k  -> 0이하면 죽은 애들
    locKnight = {i:[] for i in range(1, N+1)} # knight 좌표
    answer = {i:0 for i in range(1, N+1)}

    for i in range(1, N+1):  # 기사들의 정보
        r, c, h, w, k = map(int, input().split())
        physical[i] = k
        r, c = r - 1, c -1

        for dr in range(r, r+h):
            for dc in range(c, c+w):
                knight[dr][dc] = i
                locKnight[i].append((dr, dc))

    for _ in range(Q):
        i, d = map(int, input().split())
        knight, locKnight, no, flag = moveKnight(knight, locKnight, i, d)

        if flag:
            answer, knight = damage(locKnight, knight, answer, i, no)

    sum = 0
    for i in range(1, N+1):
        if physical[i]>0:
            sum += answer[i]
    print(sum)