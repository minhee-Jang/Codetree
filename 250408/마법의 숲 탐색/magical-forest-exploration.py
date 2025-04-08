from collections import deque
def get_rowmax(forest, r, c, d, gol_inx):   #DFS
    r, c = r - 2, c
    row_max = r + 1  # 본인 위치에서 갈 수 있는 최대
    visited = [[False] * (C+1) for _ in range(R-2)]
    map_f = []
    map_gi = []
    for i in range(2, R):  # R=9
        map_f.append(forest[i])
    for i in range(2, R):  # R=9
        map_gi.append(gol_inx[i])
    for dr, dc in gol:
        visited[r+dr][c+dc] = True #본인 골렘은 갈필요 x

    myque = deque()
    myque.append((r + gol[d][0], c+ gol[d][1], 2))  ## 출구위치에서 시작하면 무조건 같은방향 한번 더 가야함
    while myque:
        start_r, start_c, gate = myque.popleft()
        for dr, dc in gol:   # 이동할 곳 탐색
            nex_r, nex_c = start_r + dr, start_c + dc
            if 0<nex_r<=R-3 and 0<nex_c<=C:
                if gate == 2: #출구위치라면
                # 아직 방문 x 골렘 위치, 어디든 이동 가능
                    if (visited[nex_r][nex_c] == False and map_f[nex_r][nex_c] !=0):
                        visited[nex_r][nex_c] = True
                        myque.append((nex_r, nex_c, map_f[nex_r][nex_c])) #다음 위치 탐색
                        row_max = max(row_max, nex_r)
                elif gate ==1: # 그냥 골렘이라면 같은 골렘 내부만 돌 수 있음
                    if (visited[nex_r][nex_c] == False and map_f[nex_r][nex_c] !=0) and (map_gi[start_r][start_c] == map_gi[nex_r][nex_c]):
                        visited[nex_r][nex_c] = True
                        myque.append((nex_r, nex_c, map_f[nex_r][nex_c])) #다음 위치 탐색
                        row_max = max(row_max, nex_r)
    return row_max

def possible(direct, r, c):
    direction = finds[direct]
    for dr, dc in direction:  # 남쪽 탐색
        fr, fc = r + dr, c + dc  # 이동할 좌표 위치 탐색
        if 0<fr<R and 0<fc<=C: # 만약에 fr fc 이동 가능
            if forest[fr][fc] !=0: # 이미 있음
                return False
        else: # index 밖 범위는 이동 불가
            return False
    return True

def find_forest(forest, g_d, ci, answer, i, gol_inx): #숲이랑 골렘의 출구방향

    r, c = 1, ci    #골렘 시작 위치 (중심)  - 골렘 0행부터 시작
    while True:  #남쪽으로 계속 하강 먼저
        if r == R - 2:  # 중심위치 최대면
            for dr, dc in gol:
                forest[r + dr][c + dc] = 1  # 위치저장
                gol_inx[r + dr][c + dc] = i
            forest[r + gol[g_d][0]][c + gol[g_d][1]] = 2  # 출구위치 별도 저장
            value = get_rowmax(forest, r, c, g_d, gol_inx)
            answer += value

            return forest, answer, gol_inx, i
        else:
            if possible(0, r, c): #남쪽 이동 가능
                 r, c = r + 1, c

            elif possible(1, r, c) and possible(0, r, c-1): #서쪽 + 남쪽 이동 가능
                r, c = r +1 , c - 1 # 이동
                if g_d == 0:
                    g_d = 3
                else:
                    g_d = g_d - 1

            elif possible(2, r, c) and possible(0, r, c+1): # 동쪽 + 남쪽 이동가능
                r, c = r +1 , c + 1 # 동쪽 아래로 이동
                g_d = (g_d + 1) % 4

            else:  # 갈 곳 없으면
                for dr, dc in gol:
                    if r+dr<=2: #몸통 밖에 나가는지 확인
                        forest = [[0 for _ in range(C + 1)] for _ in range(R)]
                        gol_inx = [[0 for _ in range(C + 1)] for _ in range(R)]
                        i = 0
                        return forest, answer, gol_inx, i

                    forest[r+dr][c+dc] = 1 #위치저장
                    gol_inx[r + dr][c + dc] = i
                forest[r+gol[g_d][0]][c+gol[g_d][1]] = 2   #출구위치 별도 저장

                #최대위치 조사 후 저장
                value = get_rowmax(forest, r, c, g_d, gol_inx)
                answer += value

                return forest, answer, gol_inx, i

def main():
    global forest, answer, gol_inx, i
    i=1
    for c_i, di in com:
        forest, answer, gol_inx, i = find_forest(forest, di, c_i, answer, i, gol_inx) # 숲 탐색
        i+=1
    print(answer)

if __name__=="__main__":
    R, C, K = map(int, input().split())
    R += 3
    com= []
    for _ in range(K):
        d, c = map(int, input().split())
        com.append((d, c))

    gol = [(-1, 0), (0, 1), (1,0), (0,-1), (0,0)]   #골렘의 index 탐색하기 위한 북-동-남-서
    forest = [[0 for _ in range(C+1)] for _ in range(R)]  #숲 -> 0 index로 출발 준비
    gol_inx = [[0 for _ in range(C + 1)] for _ in range(R)]  # 숲 -> 0 index로 출발 준비
    find_south = [(1, -1), (2, 0), (1, 1)]
    find_left =  [(-1, -1), (0, -2), (1, -1)]
    find_right =  [(-1, 1), (0, 2), (1, 1)]
    find_max = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    finds = [find_south, find_left, find_right]
    answer = 0
    main()





