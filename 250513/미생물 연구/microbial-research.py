# Q번의 실험 -> i=0일때는 0 출력일수밖에
# 미생물 투입
# Put 이후 결과 계속 업데이트 해야함 -> 좌표 index도 업데이트
from collections import deque
def putOrgan(p, s, new, b, i): # 좌표리스트, 넓이 리스트, 미생물, 보드판, index
    r1, c1, r2, c2 = new  # 새로운 미생물 받고
    s[i][0] = (r2 - r1) * (c2 - c1)   # 넓이 저장
    
    flag = False
    for r in range(r1, r2):
        for c in range(c1, c2): # 해당 영역에 put 
            if b[r][c] == 0: #빈자리
                b[r][c] = i
                
            else:  # 빈자리 아니면 
                s[b[r][c]][0] -= 1 # 해당 index 넓이 삭감
                p[b[r][c]].remove((r, c))  # 해당 좌표는 지우기 -> O(N) *******
                b[r][c] = i
                flag = True

            # 새로운 미생물은 좌표리스트 그대로 업데이트
            p[i].append((r,c))    
    # 영역 나눠져있는지 검사 -> flag = True 일때만 (겹치는 부분 발생)
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
            # 만약에 cnt == i :
            if cnt == test: 
                return p, s
            
    return p, s

# # 배양용기
# # lambda x[0]으로 sorting 
# def moveOrang():


#     return
# # result
# def saveResult():

#     return

if __name__=="__main__":

    N, Q = map(int, input().split())

    inList = []
    pList = [[] for _ in range(Q+1)]  # 좌표만 저장
    sList = [[0, i] for i in range(Q+1) ]  # 넓이랑 index -> 넓이 기준 lambda 정렬 
    for _ in range(Q):
        r1, c1, r2, c2 = map(int, input().split())
        inList.append([r1, c1, r2, c2])  

    board = [[0 for _ in range(N)] for _ in range(N)] # 미생물 판

    d = [(0,1), (1, 0), (0, -1), (-1, 0)] 

    for i in range(1, Q+1):
        n = inList[i-1] 
        pList, sList = putOrgan(pList, sList, n, board, i)
        print(i, board)
    # 실험시작
    # for r, c, r, c-> put하면 
    # put organ -> new: 넓이/ 좌표 리스트 변환/ i=1부터 넣어라
    # move Organ -> 넓이 기준으로 좌표 이동. 좌표 리스트 업데이트 
    # result는 계산
    # 이후 다시 put organ -> 좌표리스트 그대로, 새로운 미생물만 put -> 좌표리스트, 넓이 리스트 업뎃 



 
















