# 직사각형 구할 때 넓이도 신경써야함, r, c만 신경썼다가 틀림

N, M, K = map(int, input().split())
board = [ ] # 출구랑 벽 관리
curPeo = [[[] for _ in range(N)] for _ in range(N)] # 사람관리
d4 = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 상 하 좌 우 우선순위 0123
for i in range(N):
    tmp = list(map(int, input().split())) # 한변
    board.append(tmp)
locPeo = []
for _ in range(M):
    r, c = map(int, input().split())
    locPeo.append((r-1, c-1)) # 사람 위치

er,ec = map(int, input().split())  #출구좌표
board[er][ec] = -1  #출구표시

for r, c in locPeo:
    curPeo[r][c].append("p") # 사람표시

def people_move(b, p): #board랑 peeple위치
    turn = 0 # 이번 턴 이동거리
    newP = []
    for pr, pc, in p:
        curDis = abs(pr - er) + abs(pc - ec)   # 지금 위치랑 출구 거리
        for dr, dc in d4:
            nr, nc = pr + dr, pr + dc   # 탐색 위치
            nexDis = abs(nr - er) + abs(nc - ec)    #다음위치랑 출구 거리
            if 0<=nr<N and 0<=nc<N: #좌표 갈 수 있고
                if b[nr][nc] == 0 and curDis>nexDis: # 벽이 아니고 거리가 더 짧아지는 조건이면
                    turn += 1
                    newP.append((nr, nc)) #다음거리
                    break # 이동가능하면 바로 옮김

                elif b[nr][nc] == -1: #출구라면
                    turn +=1
                    break  #사람 넣을 필요 없음
        # 이동못함
        newP.append((pr, pc))

    return newP, turn

def find_rect(p, er, ec): #board랑 people
    minRect = []
    for r, c in p:
        maxr = max(r, er)
        minr = min(r, er)
        maxc = max(c, ec)
        minc = min(c, ec)    # 현재 사람과 탈출구 간 min max 뽑아놓음

        # 제일 괜찮은 애로 업데이트
        #한변의 길이
        n = max(maxr-minr, maxc-minc)   #한변의 길이

        # r과 c가 작은 순으로
        minr = min(maxr-n, 0)
        minc = min(maxc-n, 0)
        maxr = minr + n
        minc = minc + n    # 최종 정사각형

        minRect.append((n, minr, minc))  # 넓이-> 좌표순

    minRect = sorted(minRect)
    n, rr, rc = minRect[0]
    return n, rr, rc

def rotate(n, rr, rc, b, cp, er, ec):
    newb = b

    for i in range(rr+n):
        for j in range(rc+n):
            #출구, 벽 회전
            if b[i][j] >0: #벽이있다면
                newb[j][n-i-1] = b[i][j] -1  # 시계방향 90도 회전 - 내구도 감소
            else: #벽이 없다면
                if b[i][j] == -1: #출구라면
                    er, ec = j, n-i-1   #새로운 좌표로 업데이트
                newb[j][n-i-1] = b[i][j]  #그냥 0과 -1 업데이트

            #사람회전
            if cp[i][j]: # 사람있는 곳이라면
                tmp = cp[i][j]
                ni, nj = j, n-i-1   #새로운 좌표로
                if cp[ni][nj]: # 새 좌표에도 사람이 있다면
                    cp[ni][nj] += tmp  #합치고
                else:
                    cp[i][j] = [] #초기화
                    cp[ni][nj] = tmp  #옮겨심기

    return newb, er, ec, cp    #새로운 board, er, ec, curPeop

exitPeople = 0
answer = 0
uplocPeo = locPeo
upcurPeo = curPeo
updateBoard = board
count = 0
flag = True

for _ in range(K):
    uplocPeo, ans = people_move(updateBoard, uplocPeo)  #사람이동
    rectN, rectr, rectc = find_rect(uplocPeo, er, ec)  #rectangle 좌표
    updateBoard, er, ec, upcurPeo = rotate(rectN, rectr, rectc, updateBoard, upcurPeo, er, ec)

    answer += ans
    if count == M: #사람수만큼 탈출했으면
        print(answer)
        print(er, ec)
        flag = False
        break
if flag:
    #답구하고 종료
    print(answer)
    print(er, ec)
