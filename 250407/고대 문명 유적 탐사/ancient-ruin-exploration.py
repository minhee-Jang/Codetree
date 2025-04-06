from collections import deque
import copy
def BFS(place):  #유물검사 찾기 25*4방향 = 100번
    mystack = []
    #stack에 하나씩 넣을텐데, 지금 스택이랑 주변 4방향 노드 중에 숫자 겹치면
    visited = [[False for _ in range(5)] for _ in range(5)]
    ancient = []
    trace = []
    for i in range(0,5):
        for j in range(0, 5):  # 25번 x 25번 BFS = 625
            if visited[i][j] == False:
                visited[i][j] = True  # 현재좌표 방문표시
                mystack.append((i, j))
                ancient.append((i, j))
                trace.append((j, -i))
                count = 1
                while ancient:
                    cur_r, cur_c = ancient.pop()
                    #같은거 있으면 BFS 탐색 / 탐색 후 방문 표시
                    for (r, c) in dir:
                        n_r, n_c = cur_r +r, cur_c + c   #다음
                        if (0<=n_r<5 and 0<=n_c<5) and place[cur_r][cur_c] == place[n_r][n_c]:  #같은 조각일때
                            if visited[n_r][n_c] == False:
                                ancient.append((n_r, n_c))
                                trace.append((n_c, -n_r))
                                visited[n_r][n_c] = True  #방문표시
                                count +=1

                if count<3:  #유물아니면
                    del trace[-count:]  #들어온애들 없애주기

    return  len(trace), trace


def rotate_90(r, c, place): #각 좌표에서 rotate 90* 연속으로 해서 90~360도 원상복구 해야할듯
    arr = [row[c-1:c+2] for row in place[r-1:r+2]]

    new_90 = [[0] * 3 for _ in range(3)]   # 90도 회전
    for i in range(3):      #9
        for j in range(3):
            new_90[j][3 - i - 1] = arr[i][j]

    for i in range(3):   #
        for j in range(3):
            place[r+i-1][c+j-1] = new_90[i][j]

    return place

def gen_find(trace, f_max, flag):

    trace = sorted(trace)  #정렬알고리즘   열번호, - 행번호
    for i, j in trace:
        i, j = -j, i
        f_max[i][j] = gen.pop()   #하나씩 교체하기

    value, trace = BFS(f_max)  # 다시 탐색
    #있으면 value값 flag = True
    if value == 0:
        flag = False
    elif value>0:
        flag = True

    return value, flag, f_max, trace

def first_find(place):
    find_max = [(0, 0)]
    k_turn = 0
    for i in range(1,4):
        for j in range(1,4):     #격자 회전 가능 범위 9개       # 시간복잡도: 9* 625*9
            test_map = copy.deepcopy(place)
            for k in range(1, 5):
                test_map = rotate_90(i, j, test_map)  # N = 9
                value, trace = BFS(test_map)   # 625 
                if k != 4:  # 원상복구 아니면
                    if find_max[-1][0] < value or find_max[-1][0] ==0:  # 최대값보다 높으면 #초기화
                        find_max = []
                        test_map_copy = [row[:] for row in test_map]
                        find_max.append((value, 90*k, j, i, trace, test_map_copy))
                    elif find_max[-1][0] == value:  # 같으면
                        test_map_copy = [row[:] for row in test_map]
                        find_max.append((value, 90 * k, j, i, trace, test_map_copy))

    flag = True
    if len(find_max)>0:
        find_max = sorted(find_max)
        k_turn += find_max[0][0]
        f_max = find_max[0][-1]
        f_trace = find_max[0][-2]
        while flag:                      # 최대 시간복잡도 N=100   , 총 62500
            v, flag, f_max, f_trace = gen_find(f_trace, f_max, flag)    # 625
            k_turn += v
    else:
        return 0
    return k_turn, f_max

def main(fmap):
    answer = []
    f_max = fmap
    for k in range(K): #k만큼
        value, f_max = first_find(f_max)
        if value == 0:
            print(*answer)
            exit()
        answer.append(value)
    print(*answer)

if __name__=='__main__':

    K, M = map(int, input().split())
    fmap = [[] for _ in range(5)]  # index 0~4로만 있음 주의
    for i in range(5):
        fmap[i] = list(map(int, input().split()))
    gen = list(map(int, input().split()))
    gen.reverse()  # 꺼내쓸땐 -1로 뒤에부터
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    #first_find(fmap)

    main(fmap)
    #print(*ans)