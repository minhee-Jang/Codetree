D = [(-1, 0), (0, 1), (1, 0), (0, -1)] # 상 우 하 좌
def inrange(r, c, dr, dc, d):
    if 0<=r+dr<N and 0<=c+dc<N:
        return r + dr, c + dc, d
    else:
        if d==0: d =2
        elif d==1: d=3
        elif d==2: d=0
        else: d=1
        return r - dr, c - dc, d

def pickGun(gun, gOption, game, nr, nc, i):

    maxGun = max(gOption)
    if gun[i] == 0:  # p는 총 없음
        gun[i] = maxGun
        gOption.remove(maxGun)
    else:  # 보유한 총 있음
        if gun[i] < maxGun:
            gOption.append(gun[i])
            gun[i] = maxGun
            gOption.remove(maxGun)
    game[nr][nc] = gOption[:]

    return gun, game

def move(player, i, game): # 사람 있는지 확인, 그리고 업데이트
    global pLoc, gun
    ((r, c), d, s) = player[i]
    nr, nc, d = inrange(r, c, D[d][0], D[d][1], d) # 다음 이동방향

    if pLoc[nr][nc] >0: # P 있음
        pLoc[r][c] = 0
        pLoc[nr][nc] = (i, pLoc[nr][nc])
        player[i] = ((nr, nc), d, s)  # 업뎃
        return game, player, True
    else:
        pLoc[nr][nc] = i
        pLoc[r][c] = 0
        player[i] = ((nr, nc), d, s) # 업뎃
        # 해당칸에 총이 있는지 확인, 총이 이미 잇는 경우에는 공격력이 더 쎈 총 획득, 총이 없는 경우에는 총 획득
        gOption = game[nr][nc][:]
        if gOption: # 총있음
            gun, game = pickGun(gun, gOption, game, nr, nc, i)  # 한줄로

    return game, player, False

def fight(player, i, gun, game):
    global ans
    (cr, cc), cd, cs = player[i] # 이동한 사람 위치
    p1, p2 = pLoc[cr][cc] # 만난 사람
    (er, ec), ed, es = player[p2]  # 기존에 있던 사람ㄴ

    cAtt = (gun[p1] + cs, cs) # 총 + 초기 능력치
    eAtt = (gun[p2] + es, es)

    if cAtt>eAtt: win, lose = p1, p2
    else: win, lose = p2, p1
    ans[win] = (gun[win] + player[win][2]) - (gun[lose] + player[lose][2])

    # loser -> 총을 내려놓고, 원래 가진 방향대로 이동, 다른플레이어나 격자 범위 바깥이면 오른족으로 90 회전. 이동 후 pickgun
    if gun[lose] !=0:
        game[er][ec].append(gun[lose])
    gun[lose] = 0
    for a in range(player[lose][1], player[lose][1]+4):
        i = a%4
        dr, dc = D[i][0], D[i][1]
        nr, nc = er+dr, ec+dc
        if (0<=nr<N and 0<=nc<N) and pLoc[nr][nc]==0: # 이동가능
            player[lose]  = ((nr, nc), i, player[lose][2]) # 이동
            pLoc[nr][nc] = lose
            if game[nr][nc]: # 총있으면
                g = max(game[nr][nc])
                gun[lose] = g
                game[nr][nc].remove(g)
            break

    gOption = game[player[win][0][0]][player[win][0][1]][:] # 총 옵션
    
    if gOption:
        gun, game = pickGun(gun, gOption, game, player[win][0][0], player[win][0][1], win)
    pLoc[player[win][0][0]][player[win][0][1]] = win

    return  gun, game

if __name__ == '__main__':

    N, M, K = map(int, input().split())
    game = [[[] for _ in range(N)] for _ in range(N)]
    player = {i:((0, 0), 0, 0) for i in range(1, M+1)}
    gun = {i: 0 for i in range(1, M + 1)}
    pLoc = [[0 for _ in range(N)] for _ in range(N)]
    ans = [0 for _ in range(M+1)]

    for i in range(N):
        t = list(map(int, input().split()))
        for j in range(N):
            if t[j] !=0:
                game[i][j].append(t[j])

    for i in range(1, M+1):
        x, y, d, s = map(int, input().split())
        player[i] = ((x-1, y-1), d, s)
        pLoc[x-1][y-1] = i

    for k in range(K):
        for i in range(1, M+1): # 모든 플레이어 이동
            game, player, anyone = move(player, i, game)
            if anyone: # 싸움 시작
                gun, game = fight(player, i, gun, game)

    print(*ans[1:])