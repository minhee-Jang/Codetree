RuDirect = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]  #8
SanDirect = [(-1, 0), (0, 1), (1, 0), (0, -1)] #상우하좌

def chainSanta(curP, nr, nc, dr, dc, game, killSanta): # 밀려날 곳, 방향, game
    global santa
    nextP = game[nr][nc]  # 밀려나야할 곳에 앉아있는 산타
    flag = True

    while flag:
        r, c = nr + dr, nc +dc
        game[nr][nc] = curP # 현재 산타 다음 위치로 이동
        santa[curP] = (nr, nc)
        curP = nextP
     
        if 0 <= r < N and 0 <= c < N:
            if game[r][c]> 0: # 또 산타가 있음
                nextP = game[r][c]
                game[r][c] = curP  # 다음 산타
                nr, nc = r, c
            else: # 산타 없음
                game[r][c] = curP
                flag = False

            santa[curP] = (r, c)
        else: #탈락 발생
            killSanta.append(curP)
            flag = False

    return game, killSanta

def moveRudolph(game, r, c, killSanta, sleep, score):  #
    global santa

    survival = []
    for i in range(1,P+1):
        if i not in killSanta:
            survival.append((i, santa[i][0], santa[i][1]))
    mindist = N*N
    for i in range(len(survival)):
        p, pr, pc = survival[i]
        for j in range(8):
            Rr, Rc = r + RuDirect[j][0], c + RuDirect[j][1]  # 루돌프 위치 탐색
            if 0<=Rr<N and 0<=Rc<N:
                dist = (Rr - pr) **2 + (Rc - pc)**2
                if dist < mindist: #더 작다면
                    gowhere = [(pr, pc, Rr, Rc)]
                    mindist = dist
                elif dist == mindist:
                    gowhere.append((pr, pc, Rr, Rc))

    # 좌표 뽑기 -> 충돌하는 상황 고려 -> santa, sleep 고려해줘야함
    sortGoWhere = sorted(gowhere, key=lambda x: (-x[0], -x[1]))
    nr, nc = sortGoWhere[0][2], sortGoWhere[0][3]
    if game[nr][nc]>0: # 이동위치에 산타가 있으면
        dr, dc = (nr - r) , (nc - c)  #방향
        if 0<=nr+dr*C<N and 0<=nc+dc*C<N:
            if game[nr+dr*C][nc+dc*C]>0 : 
                sr, sc = nr + dr*C, nc + dc*C
                game, killSanta = chainSanta(game[nr][nc], sr, sc, dr, dc, game, killSanta)
            else:  
                santa[game[nr][nc]] = (nr + dr*C, nc + dc*C)
                game[nr + dr * C][nc + dc * C] = game[nr][nc]

            sleep.append([game[nr][nc], 2])  # 기절 산타
            score[game[nr][nc]] += C
            game[nr][nc] = 0
        else:
            killSanta.append(game[nr][nc])
            score[game[nr][nc]] += C
            game[nr][nc] = 0

    #루돌프 위치 업뎃
    game[r][c] = 0
    game[nr][nc] = -1  #

    return nr, nc, game, sleep, score, killSanta 

def moveSanta(game, Rr, Rc, killSanta, sleep, score):
    global santa

    sleeping = []  # 현재 턴 기절
    for i in range(len(sleep)):
        sleeping.append((sleep[i][0]))

    survival = []
    for i in range(1, P + 1):
        if i not in killSanta:
            survival.append((i, santa[i][0], santa[i][1]))

    for i in range(len(survival)): #탈락한 산타 없음
        p, pr, pc = survival[i]

        if p not in sleeping:  # 기절 아니라면 진행
            mindist = N*N
            flag = False
            for j in range(4):
                Sr, Sc = pr + SanDirect[j][0], pc + SanDirect[j][1]
                if 0<=Sr<N and 0<=Sc<N: # 이동 가능
                    if game[Sr][Sc] <= 0:  # 다른 산타가 있으면 갈 수 없음
                        dist = (Rr - Sr) **2 + (Rc - Sc)**2
                        curdist = (Rr - pr) **2 + (Rc - pc)**2

                        if curdist>dist and dist<mindist:  #거리가 작아지면 바로 update
                            nr, nc = Sr, Sc #움직일 좌표
                            flag = True
                            mindist = dist
                            #print(p, nr, nc, '로 이동')

            if flag: # 이동가능
                if game[nr][nc] == -1: # 루돌프 있으면 충돌
                    dr, dc = (pr - nr), (pc - nc)
                   
                    if 0 <= nr + dr * D < N and 0 <= nc + dc * D < N:  # 밀려남
                        # 여기에도 산타가 있으면
                        if game[nr+dr*D][nc+dc*D]>0:
                            sr, sc = nr + dr * D, nc + dc * D
                            game, killSanta = chainSanta(p, sr, sc, dr, dc, game, killSanta)
                        else: # 없으면
                            game[nr+dr*D][nc+dc*D] = p # 산타 이동
                            santa[p] = (nr+dr*D, nc+dc*D)
                        game[pr][pc] = 0
                        sleep.append([p, 2])
                    else:
                        killSanta.append(p)
                        game[pr][pc] = 0

                    score[p] += D
                else: # 산타가 있는 경우는 없음
                    santa[p] = (nr, nc)
                    game[nr][nc] = p
                    game[pr][pc] = 0

    return game, sleep, score, killSanta # 루돌프의 위치, Game map Update , 기절된 애들 받아줘야함


if __name__=="__main__":  #index 주의

    N, M, P, C, D = map(int, input().split())
    Rr, Rc = map(int, input().split())
    Rr, Rc = Rr -1 , Rc -1

    santa = {p:(0,0) for p in range(1, P+1)}   # 번호, 위치2
    score = [0 for _ in range(P+1)]  #산타의 점수
    game = [[0 for _ in range(N)] for _ in range(N)]
    sleep = []

    for _ in range(P):
        n, r, c = map(int, input().split())
        santa[n] = (r-1, c-1)
        game[r-1][c-1] = n
    game[Rr][Rc] = -1 #루돌프


    killSanta = []  #index로 들어가기 1~P

    for _ in range(M):

        Rr, Rc, game, sleep, score, killSanta = moveRudolph(game, Rr, Rc, killSanta, sleep, score)
        game, sleep, score, killSanta = moveSanta(game, Rr, Rc, killSanta, sleep, score)

        #턴이 종료하면

        new = []
        for i in range(len(sleep)):
            if sleep[i][1]>1:
                sleep[i][1] -= 1
                new.append(sleep[i])  # 2 이상 append. 1이면 자연소멸
        sleep = new

        if len(killSanta) ==P:
            break

        for i in range(1, P+1):
            if i not in killSanta:
                score[i] += 1

    print(*score[1:])   # 정답 출력