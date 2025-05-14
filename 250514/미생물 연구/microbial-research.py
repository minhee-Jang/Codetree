# Q번의 실험 -> i=0일때는 0 출력일수밖에
# 미생물 투입
# Put 이후 결과 계속 업데이트 해야함 -> 좌표 index도 업데이트
from collections import deque
def putOrgan(p, s, new, b, i): # 좌표리스트, 넓이 리스트, 미생물, 보드판, index
    r1, c1, r2, c2 = new  # 새로운 미생물 받고
    s[i][0] = (r2 - r1) * (c2 - c1)   # 넓이 저장
    
    flag = False
    for r in range(r1, r2):   # r2 c2가 하나씩 더 크게 들어옴 
        for c in range(c1, c2): # 해당 영역에 put 
            if b[r][c] == 0: #빈자리
                b[r][c] = i
                
            else:  # 빈자리 아니면 
                s[b[r][c]][0] -= 1 # 해당 index 넓이 삭감
                p[b[r][c]].remove((r, c))  # 해당 좌표는 지우기 -> O(N) *******
                b[r][c] = i
                flag = True

            p[i].append((r,c))    

    # 영역 나눠져있는지 검사 -> flag = True 일때만 (겹치는 부분 발생)
    if flag:
        test = sum(1 for sub in p if sub)
        delList = []
        visited = [[False for _ in range(N)] for _ in range(N)] # DFS 
        q = deque()
        cnt = 0
        for r in range(N):  
            for c in range(N):  
                # 방문한 곳 아닐때 
                if visited[r][c] == False:
                    if b[r][c] != 0 and b[r][c] not in delList: # 숫자가 있고, 지워지는 리스트에도 없을때 -> 검사 필요. 지워지는 리스트에 있으면 검사할 필요 x
                        q.append((r, c))  
                        cur = b[r][c] # 현재 index와 같은 애들만 취급
                        visited[r][c] = True
                        size = 1
                        # BFS(같은숫자만) 
                        while q:
                            r, c = q.popleft() 
                            for dr, dc in d:
                                nr, nc = r + dr, c + dc  # 다음 좌표
                                if 0<=nr<N and 0<=nc<N:
                                    if b[nr][nc] == cur and visited[nr][nc] == False: # 같은애들만
                                        q.append((nr, nc))
                                        size += 1
                                        visited[nr][nc] = True
                    # 만약에 넓이 안같으면 그냥 지워버리기, 좌표리스트랑 넓이리스트에서 삭제, dellist 에 추가
                        if size != s[cur][0]: 
                            s[cur][0]=0
                            # 좌표 따라서 0으로 만들기 
                            for x, y in p[cur]:
                                if b[x][y] != cur:
                                    visited[x][y] = False  
                                b[x][y] = 0
                            p[cur] = [] 
                            delList.append(cur)  # 없어진 미생물 리스트 
                    # 검사횟수 카운트
                        cnt += 1 
                    else:
                        visited[r][c] = True

                if cnt == test: 
                    return p, s
            
    return p, s

# 배양용기 -> r , c 가 작은 순으로 배치해야함
# lambda x[0]으로 sorting 
def moveOrgan(p, s): 
    newBoard = [[0 for _ in range(N)] for _ in range(N)] # 미생물 판
    s = sorted(s, key=lambda x: (-x[0], x[1])) # 0은 내림차순, 1은 오름차순 (먼저투입된 순서)
    
    # s[i][0] 값이 > 0 이면 배치 -> 좌표 리스트에서 r1, c1, r2, c2 뽑아서 공간 확보ㅛ
    # for r, c visited 이용 -> board 잘라서 배치 가능한지 확인 (안되면 패스) -> 자르기 가능하면 원소 확인 후 배치하고, 좌표 업뎃 -> 불가능하면 좌표리스트에서 삭제, 넓이는 0으로 만듦
    for i in range(len(s)):
        sd, id = s[i]
        if sd>0 and p[id]:
            minr = min(p[id], key=lambda x:x[0])[0]
            minc = min(p[id], key=lambda x:x[1])[1]
            maxr = max(p[id], key=lambda x:x[0])[0]
            maxc = max(p[id], key=lambda x:x[1])[1]

            lr = maxr - minr # 행길이
            lc = maxc - minc # 열길이
            placed = False
            for c in range(N): 
                for r in range(N): 
                    if r + lr< N and c + lc < N: # 자르기 가능
                        subgrid = [row[c:c+lc+1] for row in newBoard[r:r+lr+1]]
                        # total = sum(sum(row) for row in subgrid)
                        # 임의로 배치 해보기 
                        sr, sc = minr , minc  
                        for a, b in p[id]: # 해당 좌표 리스트에서 
                            if subgrid[a - sr][b - sc] == 0: 
                                placed = True
                            else:
                                placed = False
                                break

                        if placed:  # 배치 가능
                            dr, dc = minr - r, minc - c
                            newp = []
                            for a, b in p[id]: # 해당 좌표 리스트에서 
                                newBoard[a - dr][b - dc] = id  # 이동
                                newp.append((a - dr, b - dc))
                            p[id] = newp  # 좌표 업뎃
                            placed = True
                            break
                if placed:
                    break
            # 배치 불가능하면 제거
            if not placed:
                p[id] = [] 
                s[i][0] = 0
 
    return p, s, newBoard

# result
def saveResult(b):
    ans = []
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[0][0] = True

    for r in range(N):
        for c in range(N):
            cur = b[r][c]  # 현재 index
            visited[r][c] = True
            for dr, dc in d:
                nr, nc = r + dr, c + dc
                if (0<=nr<N and 0<=nc<N) and (cur !=0 and b[nr][nc] !=0):  # 둘다 0 아니어야
                    if cur != b[nr][nc]: # 경계면 확인 
                        if ((cur, b[nr][nc]) not in ans) and ((b[nr][nc], cur) not in ans):
                            ans.append((cur, b[nr][nc]))

    return ans

if __name__=="__main__":

    N, Q = map(int, input().split())
    # 입력이 c1, r1, c2, r2로 들어오고있음 
    inList = []
    pList = [[] for _ in range(Q+1)]  # 좌표만 저장
    sList = [[0, i] for i in range(Q+1) ]  # 넓이랑 index -> 넓이 기준 lambda 정렬 
    for _ in range(Q):
        c1, r1, c2, r2 = map(int, input().split())
        inList.append([r1, c1, r2, c2])  

    board = [[0 for _ in range(N)] for _ in range(N)] # 미생물 판

    d = [(0,1), (1, 0), (0, -1), (-1, 0)] 

    for i in range(1, Q+1):
        n = inList[i-1] 
        pList, sList = putOrgan(pList, sList, n, board, i) 
        #print(board)
        pList, sList, board = moveOrgan(pList, sList) 
        #print(board)
        sList = sorted(sList, key=lambda x:x[1])  #index 정렬
        touchList = saveResult(board) 
        #print(touchList)
        answer = 0
        #print(sList)
        if touchList:
            for id1, id2 in touchList:
                answer += sList[id1][0] * sList[id2][0]
        print(answer)
