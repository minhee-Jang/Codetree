# 튜플 순서대로 비교하는 거로 짠 ver

def is_inrange(x, y):
    return 1<=x and x<=n and 1<=y and y<=n

n, m, p, c, d = map(int, input().split())
rudolf = tuple(map(int, input().split()))

points = [0 for _ in range(p + 1)]   #점수
pos = [(0, 0) for _ in range(p + 1)] #각 산타 위치
board = [[0 for _ in range(n + 1)] for _ in range(n + 1)] #게임판
is_live = [False for _ in range(p + 1)] #생존여부
stun = [0 for _ in range(p + 1)] # 기절여부

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]  #상우하좌

board[rudolf[0]][rudolf[1]] = -1  # 루돌프 초기 위치


for _ in range(p):
    id, x, y = tuple(map(int, input().split()))
    pos[id] = (x, y)
    board[pos[id][0]][pos[id][1]] = id
    is_live[id] = True

for t in range(1, m + 1):   #M번의 turn
    closestX, closestY, closestIdx = 10000, 10000, 0
    #가까운 산타 찾기
    for i in range(1, p+1):
        if not is_live[i]:
            continue

        currentBest = ((closestX - rudolf[0])**2 + (closestY - rudolf[1])**2, (-closestX, -closestY))
        currentValue = ((pos[i][0] - rudolf[0])**2 + (pos[i][1] - rudolf[1])**2, (-pos[i][0], -pos[i][1]))

        if currentValue < currentBest:
            closestX, closestY = pos[i]
            closestIdx = i
    # 루돌프의 이동
    if closestIdx:
        prevRudolf = rudolf
        moveX = 0
        # 8방향 가능이기 때문에, 작은지 큰지만 비교해도 됨
        if closestX > rudolf[0]:
            moveX = 1
        elif closestX < rudolf[0]:
            moveX = -1

        moveY = 0
        if closestY > rudolf[1]:
            moveY = 1
        elif closestY < rudolf[1]:
            moveY = -1

        # 루돌프 최종 이동
        rudolf = (rudolf[0] + moveX, rudolf[1] + moveY)
        board[prevRudolf[0]][prevRudolf[1]] = 0

    # 루돌프 이동 중 산타 충돌 -> 같은 방향으로 산타 이동
    if rudolf[0] == closestX and rudolf[1] == closestY:
        firstX = closestX + moveX * c
        firstY = closestY + moveY * c
        lastX, lastY = firstX, firstY

        stun[closestIdx] = t + 1 #기절 날짜

        #마지막으로 이동한 위치에 산타  -> 어디까지 연쇄 충돌이 일어날건지
        while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
            lastX += moveX
            lastY += moveY

        # 연쇄 충돌의 가장 마지막 위치에서 시작함 -> 순차적으로 이동
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY

            if not is_inrange(beforeX, beforeY):
                break

            idx = board[beforeX][beforeY]

            if not is_inrange(lastX, lastY):  #나가면 탈락
                is_live[idx] = False
            else: # 한칸씩 이동
                board[lastX][lastY] = board[beforeX][beforeY]
                pos[idx] = (lastX, lastY)

            lastX, lastY = beforeX, beforeY

        points[closestIdx] += c  # 점수 획득

        # 연쇄충돌 아닐 때
        pos[closestIdx] = (firstX, firstY)
        if is_inrange(firstX, firstY):
            board[firstX][firstY] = closestIdx
        else:
            is_live[closestIdx] = False

    # 루돌프 최종 이동
    board[rudolf[0]][rudolf[1]] = -1


    # 산타 이동
    for i in range(1, p+1):
        if not is_live[i] or stun[i]>=t:   #t+1로 다음날까지 기절하게 셋팅
            continue

        minDist = (pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2
        moveDir = -1

        for dir in range(4):
            nx = pos[i][0] + dx[dir]
            ny = pos[i][1] + dy[dir]

            if not is_inrange(nx, ny) or board[nx][ny] > 0:
                continue

            dist = (nx - rudolf[0]) ** 2 + (ny - rudolf[1]) ** 2
            if dist < minDist:
                minDist = dist
                moveDir = dir

        if moveDir != -1 : #이동할 수 있는 산타라면
            nx = pos[i][0] + dx[moveDir]
            ny = pos[i][1] + dy[moveDir]

            # 산타의 움직임으로 충돌하면
            if nx == rudolf[0] and ny == rudolf[1]:
                stun[i] = t + 1

                moveX = -dx[moveDir]
                moveY = -dy[moveDir]

                firstX = nx + moveX * d
                firstY = ny + moveY * d
                lastX, lastY = firstX, firstY

                if d == 1:  #자기 자리로 돌아감
                    points[i] += d
                else: # 연쇄 충돌 가능성
                    # 만약 이동한 위치에 산타가 있을 경우
                    while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY

                    # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작
                    while lastX != firstX or lastY != firstY:
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY

                        if not is_inrange(beforeX, beforeY):
                            break

                        idx = board[beforeX][beforeY]

                        if not is_inrange(lastX, lastY):
                            is_live[idx] = False
                        else:
                            board[lastX][lastY] = board[beforeX][beforeY]
                            pos[idx] = (lastX, lastY)

                        lastX, lastY = beforeX, beforeY

                    points[i] += d
                    board[pos[i][0]][pos[i][1]] = 0
                    pos[i] = (firstX, firstY)
                    if is_inrange(firstX, firstY):
                        board[firstX][firstY] = i
                    else:
                        is_live[i] = False
            #충돌 안하면 그냥 이동
            else:
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = (nx, ny)
                board[nx][ny] = i

    for i in range(1, p+1):
        if is_live[i]:
            points[i] += 1

for i in range(1, p+1):
    print(points[i], end=" ")

