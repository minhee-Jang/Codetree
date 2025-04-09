from collections import deque
def base_loc(plain, tar):
    for i in range(len(plain)):
        for j in range(len(plain[i])):
            if plain[i][j]== tar:
                fi, fj = i, j   # 탐색 시작위치 준비
                return fi, fj

def find_exit_3d(r2, c2, direct): #2차원에서 출구 위치
    #찾은 출구 방향 기준으러
    exi3i = M -1
    p3 = direct

    if direct ==0:
        exi3j =  (M - 1) - (r2 - bi)
    elif direct ==1: #서
        exi3j = r2 - bi
    elif direct ==2:  #남
        exi3j = c2 - bj
    else: #북
        exi3j = (M - 1) - (c2 - bj)

    return p3, exi3i, exi3j

def find_exit_2d(sr, sc):

    visited = [[False for _ in range(N)] for _ in range(N)] #visited 배열
    q = deque()
    q.append((sr, sc))

    while q:
        r, c = q.popleft()
        for i in range(4):
            nr = r + just_find[i][0]
            nc = c + just_find[i][1]
            if 0<=nr<N and 0<=nc<N:  # 3과 0만 찾으면 됨
                if space2d[nr][nc] == 3 and visited[nr][nc]==False:  #3이면
                    q.append((nr, nc))
                    visited[nr][nc] = True
                elif space2d[nr][nc] == 0 and visited[nr][nc]==False:  #탐색위치 출구이면
                    return nr, nc, i #어느 방향에서 찾았는지도
    print(-1)
    exit()

def shift_plane(cp, cr, cc):
    left = {2:1, 1:3, 3:0, 0:2}
    right = {2:0, 0:3, 3:1, 1:2}

    if cr<0: #위쪽으로 이탈
        if cp ==0: cp, cr, cc = 4, (M-1) - cc, M-1
        elif cp ==1: cp, cr, cc = 4, cc, 0
        elif cp ==2: cp, cr, cc = 4, M-1, cc
        elif cp ==3: cp, cr, cc = 4, 0, (M -1) - cc
        elif cp ==4: cp, cr, cc = 3, 0, (M -1) - cc
    elif cr>=M : # 아래쪽 범위 이탈
        if cp ==4: cp, cr, cc = 2, 0, cc
        else:
            cp, cr, cr = cp, cr -1, cc    #다시 제자리로
    elif cc<0: #왼쪽으로 이탈
        if cp==4: cp, cr, cc = 1, 0, cr
        else:
            cp, cr, cc = left[cp], cr, M-1
    elif cc>=M: #오른쪽으로 이탈
        if cp==4: cp, cr, cc = 0, 0, (M-1) - cr
        else:
            cp, cr, cc = right[cp], cr, 0
    return cp, cr, cc


def get_exit_3d(e_p, er, ec): #3d평면에서 출구 찾기
    global space3d_count

    visit_3d = [[[False for _ in range(M)] for _ in range(M)] for _ in range(5)]   #visited 배열
    sr, sc = b3i, b3j #타임머신 시작 좌표
    q3 = deque()
    q3.append((sr, sc, 4))
    visit_3d[4][sr][sc] = True

    while q3:
        r, c, p = q3.popleft()
        if r==er and c==ec and p == e_p: #탈출 위치
            return space3d_count[p][r][c]    #3D 탈출까지 도달하는 count
        for i in range(4):
            nr, nc = r + just_find[i][0], c + just_find[i][1]   #방향탐색
            if 0<=nr<M and 0<=nc<M:  #해당 플레인 안에 있으면, cp 그대로
                if visit_3d[p][nr][nc]==False and space3d[p][nr][nc]==0: # 방문도 안했고 장애물도 없으면
                    q3.append((nr, nc, p))
                    visit_3d[p][nr][nc] = True  #방문표시
                    space3d_count[p][nr][nc] = space3d_count[p][r][c] + 1
            else:
                np, nr, nc = shift_plane(p, nr, nc)
                if visit_3d[np][nr][nc] == False and space3d[np][nr][nc] == 0:
                    q3.append((nr, nc, np))
                    visit_3d[np][nr][nc] = True
                    space3d_count[np][nr][nc] = space3d_count[p][r][c] + 1


def diffusion(c, diff):
    for i in range(len(diff)):
        rv, cv, d, v = diff[i]
        turn = c
        if v!=0:
            while turn - v >= v: # 배수일 때 10, 3이면 7, 4, 1
                turn -= v
                nr, nc = rv + just_find[d][0], cv + just_find[d][1]  # 확산
                if space2d[nr][nc] == 0:
                    space2d[nr][nc] = 1  # 확산
                    diff[i] = [nr, nc, d, v]
                else:  # 확산 불가
                    diff[i] = [rv, cv, d, 0]  # 나중에 v=0이면 무시
                    break

    return diff

def mini_diff(t, diff):
    for i in range(len(diff)):
        rv, cv, d, v = diff[i]
        if v != 0:
            if t%v == 0:  #그때 그시간 배수이면
                nr, nc = rv + just_find[d][0], cv + just_find[d][1]  # 확산
                if 0<=nr<N and 0<=nc<N:
                    if space2d[nr][nc] == 0:
                        space2d[nr][nc] = 1  # 확산
                        diff[i] = [nr, nc, d, v]
                    else:  # 확산 불가
                        diff[i] = [rv, cv, d, 0]  # 나중에 v=0이면 무시
    return diff

def get_exit_2d(sr, sc, t, diff):
    time = t  #3D 완전 탈출까지 +=1 더
    visit_2d = [[False for _ in range(N)] for _ in range(N)]
    q2 = deque()
    q2.append((sr, sc))
    visit_2d[sr][sc] = True

    while q2:
        r, c = q2.popleft()
        for i in range(4):
            nr, nc = r + just_find[i][0], c + just_find[i][1] # 방향찾기
            if 0<=nr<N and 0<=nc<N:
                if visit_2d[nr][nc]==False and space2d[nr][nc]==0: #방문안하고 갈 수 있으면
                    q2.append((nr, nc))
                    visit_2d[nr][nc] = True
                    space2d[nr][nc] = space2d[r][c] + 1   #방문표시
                    diff = mini_diff(space2d[nr][nc], diff)
                elif visit_2d[nr][nc]==False and space2d[nr][nc]==4: # 출구
                    space2d[nr][nc] = space2d[r][c] + 1
                    return space2d[r][c] + 1

    #만약에 없으면
    return -1

def main():
    global space3d, space2d, bi, bj, diff
    ex2i, ex2j, d = find_exit_2d(bi, bj)     #2차원 이어지는 탈출구 위치
    exit_p, ex3i, ex3j = find_exit_3d(ex2i, ex2j, d)   #3차원에서 탈출위치

    count_3d = get_exit_3d(exit_p, ex3i, ex3j)

    # 그동안 미지의 공간 확산
    new_d = diffusion(count_3d, diff)

    space2d[ex2i][ex2j] = count_3d + 1  # 2D 탈출 시작

    answer = get_exit_2d(ex2i, ex2j,  count_3d + 1, new_d)
    print(answer)

if __name__ == "__main__":

    N, M, F = map(int, input().split())
    space2d = [[[] for _ in range(N)] for _ in range(N)]
    space3d = [[[[] for _ in range(M)] for _ in range(M)] for _ in range(5)]  #동서남북윗면 순서
    space3d_count = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)]
    #동 : 0, 서 : 1, 남 :2 북:3 윗면:4
    for i in range(N):
        space2d[i] = list(map(int, input().split()))
    for i in range(M*5):
        space3d[i//M][i%M] = list(map(int, input().split()))

    diff = []
    for _ in range(F):
        diff.append(list(map(int, input().split())))
    for rv, cv, _, _ in diff:
        space2d[rv][cv] = 1   #장애물 표시

    b3i, b3j = base_loc(space3d[-1], 2)   #윗면에서 타임머신 위치
    bi, bj = base_loc(space2d, 3)   #시공간 위치 시작점 (상대적 좌표 거리 이용)

    just_find = [(0, 1), (0, -1), (1, 0), (-1, 0)]  #동 서 남 북

    main()






