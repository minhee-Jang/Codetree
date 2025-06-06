# 점심시간 그룹 형성이 1명도 된다는 말은 없었잖아 ................................

# 민트 초코 우유 
from collections import deque
def pickBoss(f, b):  # 신봉음식, 신앙심
    boss = [[], [], []] 
    visited = [[False for _ in range(N)] for _ in range(N)]
 
    for i in range(N):
        for j in range(N):
            if visited[i][j] == False:    # 검사 시작
                cnt = 0
                group = [(b[i][j], i, j)]    #초기화

                #BFS
                q = deque() 
                q.append((i, j))
                believe = f[i][j]   # 현재 학생 신봉 음식 
                visited[i][j] = True # 방문표시
                while q:
                    r, c = q.popleft()
                    cnt += 1 
                    for dr, dc in d:
                        nr, nc = r + dr, c + dc # 다음좌표
                        if (0<=nr<N and 0<=nc<N) and visited[nr][nc] == False: # 방문 가능하면 
                            if believe == f[nr][nc]: # 신봉음식 같으면 
                                q.append((nr, nc))
                                group.append((b[nr][nc], nr, nc))  
                                visited[nr][nc] = True
                #대표 선출
                sortgroup = sorted(group, key=lambda x:(-x[0], x[1], x[2]))    # sort
                bossr, bossc = sortgroup[0][1], sortgroup[0][2]
                for _, pr, pc in sortgroup[1:]:
                    b[pr][pc] -= 1 # 그룹원들 신앙심 제거 - 신앙심은 항상 1보다 같거나 큼
                    b[bossr][bossc] += 1
                boss[len(f[bossr][bossc][0])-1].append((b[bossr][bossc], bossr, bossc))
    return boss, b    # 대표 리스트   

def makeUs(f, b, boss):  # 대표리스트, 신봉음식, 신앙심 
    defence = [[False for _ in range(N)] for _ in range(N)]
    # 대표자 우선순위 설정
    for i in range(len(boss)):
        if boss[i]:
            boss[i] = sorted(boss[i], key=lambda x:(-x[0], x[1], x[2]))   
    #print("boss", boss)
    # 전파시작
    flag = False
    for i in range(3): # 세 그룹 순서대로
        for bvalue, ar, ac in boss[i]: # 대표 전파자 정보 

            if defence[ar][ac] == False: # 방어태세 아님
                x = bvalue - 1
                direct = bvalue % 4 # 전파 방향
                b[ar][ac] = 1   # 1만 남기고
            
    #       x>y이면 강한 전파 : 전파 대상은 전파자의 사상에 완전히 동화, 동일 음식 신봉 / 전파자 y+1만큼 간절함 까임, 전파 대상은 신앙심 1 증가
    #       x<=y 이면 약한전파 : 전파 대상은 전파자가 전파한 음식의 모든 기본 음식에 관심, -> 자기꺼 + 전파자꺼 모두합친음식을 신봉 / 전파자 간절함 모두 소진, 전파 대상 신앙심은 x 만큼 증가
                br, bc = ar, ac
                while x>0: 
                    nr, nc = br + d[direct][0], bc + d[direct][1]   
                    if (0<=nr<N and 0<=nc<N) and (f[br][bc] != f[nr][nc]):  # 전파 할 수 있으묜
                        if x>b[nr][nc]: # 전파 대상의 신앙심이 간절함보다 작을때 -> 강한 전파 
                            f[nr][nc] = [f[br][bc][0]]  # 신봉 음식 동일해짐
                            #print("강한전파", f[nr][nc])
                            x -= (b[nr][nc] + 1) # 간절함 까임
                            b[nr][nc] += 1  
                        else: 
                            #newfood = ''.join(sorted(set(f[nr][nc]+f[br][bc])))
                            for a in f[br][bc][0]: # 전파 대상의 음식까지 관심을 가져야함
                                if a not in f[nr][nc][0]:
                                    f[nr][nc][0] = f[nr][nc][0] + a 
                                    #f[nr][nc].append(a)   # 없으면 추가
                            f[nr][nc] = sorted(f[nr][nc][0])
                            f[nr][nc] = [''.join(f[nr][nc])]   # 한 문자로 바꿈 
                            #print("약한전파", f[nr][nc])
                            b[nr][nc] += x
                            x = 0
                        for h in range(3):
                            for k in range(len(boss[h])):   #전파한 곳이 리더라면 방어태새 on
                                if nr == boss[h][k][1] and nc == boss[h][k][2]:
                                    defence[nr][nc] = True  # 전파된 곳 방어태세 on
                    elif (0<=nr<N and 0<=nc<N) and (f[br][bc] == f[nr][nc]):   # 갈수 있지만 전파 필요 x -> 패스
                        #print('전파불필요')
                        pass
                    elif not (0<=nr<N and 0<=nc<N):
                        #print('격자 벗어남')
                        break  # 전파 종료
                    br, bc = nr, nc  # 다음 턴

    return f, b

if __name__=="__main__":


# 입력
    N, T = map(int, input().split()) 
   
    B = [] # 신앙심
    food = [[] for _ in range(N)]  # 신봉 음식 
    
    for i in range(N):
        foodTmp = map(str, input()) 
        for s in foodTmp:
            food[i].append([s])

    for _ in range(N):
        bTmp = list(map(int, input().split()))   
        B.append(bTmp)

    # 전파 방향 0 1 2 3 위 아래 왼 오
    d = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #BFS
    
    for _ in range(T):   # T 최대 30
        # 1. 아침시간
        for i in range(N):  # 최대 2500
            for j in range(N):
                B[i][j] += 1

        # 2. 점심시간
        boss, B = pickBoss(food, B)   # 대표리스트

        # 3. 저녁시간
        food, B = makeUs(food, B, boss) 
        #CMT, CT, MT, CM, M, C, T
        ans = [0 for _ in range(7)]
        # T 민트 1 C 초코 2 M 우유 3
        for r in range(N):
            for c in range(N):
                whichfood = food[r][c][0]
                if whichfood == 'CMT': ans[0] += B[r][c]
                elif whichfood == 'CT': ans[1] += B[r][c]
                elif whichfood == 'MT': ans[2] += B[r][c]
                elif whichfood == 'CM': ans[3] += B[r][c]
                elif whichfood == 'M': ans[4] += B[r][c]
                elif whichfood == 'C': ans[5] += B[r][c]
                elif whichfood == 'T': ans[6] += B[r][c]
        
        print(*ans)