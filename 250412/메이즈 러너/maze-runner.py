# 직사각형 구할 때 넓이도 신경써야함/ r, c만 신경썼다가 틀림
# 행렬 index 틀림
# 부분 회전할 때 exit 좌표 참조해서 틀림

from copy import deepcopy
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
    locPeo.append((r-1, c-1)) # 사람 위치 좌표 리스트트

er, ec = map(int, input().split())  #출구좌표
er -= 1
ec -= 1
board[er][ec] = -1  #출구는 항상 -1

for r, c in locPeo:
    curPeo[r][c].append("p") # 사람표시
print(curPeo)
def people_move(b, p, er, ec): #board랑 peeple위치
    global count

    turn = 0 # 이번 턴 사람 이동 
    newP = []
    newcP = [[[] for _ in range(N)] for _ in range(N)]
    for pr, pc in p: 
        curDis = abs(pr - er) + abs(pc - ec)   # 현재 위치와 출구 거리
        moved = False
        for dr, dc in d4:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < N and 0 <= nc < N:
                nexDis = abs(nr - er) + abs(nc - ec)
                if b[nr][nc] == 0 and curDis > nexDis:
                    newP.append((nr, nc))
                    turn += 1
                    moved = True
                    break
                elif b[nr][nc] == -1:
                    count += 1
                    turn += 1
                    print("exit")
                    moved = True
                    break
        if not moved:
            newP.append((pr, pc))  # 이동 못 하면 제자리
    for r, c in newP: #사람 옮겨심기기
        newcP[r][c].append(("p"))

    print("move", newP)
    return newP, turn, newcP, count

def find_rect(p, er, ec): #board랑 people
    minRect = [] 
    print(p)
    for r, c in p:
        maxr = max(r, er)
        minr = min(r, er)
        maxc = max(c, ec)
        minc = min(c, ec)    # 현재 사람과 탈출구 간 min max 뽑아놓음

        # 제일 괜찮은 애로 업데이트
        #한변의 길이 
        print(maxr, minr, maxc, minc, er, ec, r, c)
        n = max(maxr-minr, maxc-minc)   #한변의 길이 
        # r과 c가 작은 순으로
        minr = max(maxr-n, 0)
        minc = max(maxc-n, 0)
        maxr = minr + n
        maxc = minc + n    # 최종 정사각형

        minRect.append((n, minr, minc))  # 넓이-> 좌표순
     
    minRect = sorted(minRect)
    (n, rr, rc) = minRect[0] 
    return n, rr, rc

def rotate(n, rr, rc, b, cp, er, ec):
    newb = b
    n+=1
    locP = []
    newcP = deepcopy(cp)
    arr = [row[rc:rc+n] for row in b[rr:rr+n]]
    testarr = deepcopy(arr)
    cp = [row[rc:rc+n+1] for row in cp[rr:rr+n+1]] 
    print("arry", arr, rr, rc, n)
    
    for i in range(0, n):
        for j in range(0, n): 
            #출구, 벽 회전
            if arr[i][j] >0: #벽이있다면
                testarr[j][n-i-1] = arr[i][j] -1  # 시계방향 90도 회전 - 내구도 감소
            else: #벽이 없다면 
                testarr[j][n-i-1] = arr[i][j]  #그냥 0과 -1 업데이트

            #사람회전
            if cp[i][j]: # 사람있는 곳이라면  
                ni, nj = j, n-i -1   #새로운 좌표로
                for _ in range(len(cp[i][j])):
                    locP.append((ni, nj)) 
                cp[i][j] = []
                
  
    for r, c in locP: #사람 옮겨심기기
        cp[r][c].append(("p"))
    
    for i in range(rr, rr+n):
        for j in range(rc, rc+n):
            newb[i][j] = testarr[i-rr][j-rc]            #2, 3일 때 0,0
            newcP[i][j] = cp[i-rr][j-rc]
            if testarr[i-rr][j-rc] == -1:
                er, ec = i, j
 
    locP = []
    for i in range(N):
        for j in range(N):
            if newcP[i][j]:
                for _ in range(len(newcP[i][j])):
                    locP.append((i, j)) 
    print('roate', locP, newcP)
    return newb, er, ec, newcP, locP    #새로운 board, er, ec, curPeop

exitPeople = 0
answer = 0
uplocPeo = locPeo
upcurPeo = curPeo
updateBoard = board
count = 0
flag = True
print(uplocPeo)
#print(upcurPeo)
for i in range(K):
    print(i)
    for j in range(N):
        print(upcurPeo[j])
        print(updateBoard[j])
    uplocPeo, ans, upcurPeo, count = people_move(updateBoard, uplocPeo, er, ec)  #사람이동
    answer += ans 
    if count == M: #사람수만큼 탈출했으면
        print(answer)
        print(er, ec)
        flag = False
        break
    rectN, rectr, rectc = find_rect(uplocPeo, er, ec)  #rectangle 좌표
    updateBoard, er, ec, upcurPeo, uplocPeo = rotate(rectN, rectr, rectc, updateBoard, upcurPeo, er, ec)

    
    
if flag:
    #답구하고 종료
    print(answer)
    print(er+1, ec+1)