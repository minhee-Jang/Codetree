from collections import deque
def inBoard(nx,ny):
    if 0<nx<=R-3 and 0<ny<=C:
        return True
    return False

def get_rowmax(forest, r, c, d, gol_inx):
    r, c = r - 2, c
    if r == R-4:  # R 6->9 -> 5까지 가능
        return r + 1

    row_max = r + 1
    visited = [[False] * (C + 1) for _ in range(R - 2)]
    map_f = forest[2:]
    map_gi = gol_inx[2:]

    for dr, dc in gol:
        visited[r + dr][c + dc] = True

    myque = deque()
    myque.append((r + gol[d][0], c + gol[d][1], 2))  # 출구에서 시작

    while myque:
        r, c, gate = myque.popleft()
        row_max = max(row_max, r)
        for dr, dc in find_max:
            n_r, n_c = r + dr, c + dc
            if not inBoard(n_r, n_c) or visited[n_r][n_c] or map_f[n_r][n_c] == 0:
                continue

            if gate == 2:
                visited[n_r][n_c] = True
                myque.append((n_r, n_c, map_f[n_r][n_c]))

            elif gate == 1:
                if map_gi[r][c] == map_gi[n_r][n_c]:
                    visited[n_r][n_c] = True
                    myque.append((n_r, n_c, map_f[n_r][n_c]))

    return row_max

def possible(direct, r, c):
    direction = finds[direct]
    for dr, dc in direction:
        fr, fc = r + dr, c + dc
        if 0<=fr<R and 0<fc<=C: # 만약에 fr fc 이동 가능
            if forest[fr][fc] !=0: # 이미 있음
                return False
        else: # index 밖 범위여도 이동 불가
            return False
    return True

def in_forest(r,c):
    return 3 <= r < R and 0 < c <= C


def find_forest(forest, g_d, ci, answer, i, gol_inx): #숲이랑 골렘의 출구방향
    r, c = 1, ci    #골렘 시작 위치 (중심)  - 골렘 0행부터 시작
    while True:  #남쪽으로 계속 하강 먼저
        if r == R - 2:  # 중심위치 최대면
            for dr, dc in gol:
                forest[r + dr][c + dc] = 1  # 위치저장
                gol_inx[r + dr][c + dc] = i
            forest[r + gol[g_d][0]][c + gol[g_d][1]] = 2  # 출구위치 별도 저장

            answer += R - 3

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

            else:  # 갈 곳 없으면 정착
                for dr, dc in gol:
                    if in_forest(r+dr, c+dc):
                        forest[r + dr][c + dc] = 1  # 위치저장
                        gol_inx[r + dr][c + dc] = i
                    else:   #골렘 빠져나감
                        forest = [[0 for _ in range(C + 1)] for _ in range(R)]
                        gol_inx = [[0 for _ in range(C + 1)] for _ in range(R)]
                        i = 0

                        return forest, answer, gol_inx, i
                #정착 가능 하면 저장되면
                forest[r+gol[g_d][0]][c+gol[g_d][1]] = 2   #출구위치 별도 저장
                #최대위치 조사 후 저장
                value = get_rowmax(forest, r, c, g_d, gol_inx)
                answer += value

                return forest, answer, gol_inx, i

def main():
    global forest, answer, gol_inx, i
    i=1
    count = 0
    for c_i, di in com:
        forest, answer, gol_inx, i = find_forest(forest, di, c_i, answer, i, gol_inx) # 숲 탐색
        i+=1
        count+=1
        # print("++++++++++++", count)
        # print(c_i, di)
        # for row in forest:
        #     print(*row)
        # print("++++++++++++")
        # for row in gol_inx:
        #     print(*row)
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





