# 최대 격자 크기를 55로 정의합니다. (인덱스를 1부터 사용하기 때문에 55로 잡습니다.)
MAX_SIZE = 55
# 4방향 (상, 하, 좌, 우) 이동을 위한 방향 벡터의 크기를 4로 정의합니다.
DIR_COUNT = 4
# 각 방향별 행 이동 변화량을 저장합니다. (상: -1, 하: +1, 좌: 0, 우: 0)
dx = [ -1, 1, 0, 0 ]
# 각 방향별 열 이동 변화량을 저장합니다. (상: 0, 하: 0, 좌: -1, 우: +1)
dy = [ 0, 0, -1, 1 ]

# 전역 변수 gridSize 는 격자의 크기를 나타내며, totalDays 는 전체 일 수를 나타냅니다.
gridSize = 0
totalDays = 0
# 초기 입력으로 받은 음식 신념 상태를 문자열 배열로 저장합니다. 
# 각 문자열은 각 행의 음식 신념 정보를 나타내며, 각 문자는 'T', 'C', 'M' 중 하나입니다.
initialFoodGrid = ["" for _ in range(MAX_SIZE+1)]
# foodGrid 배열은 각 칸의 음식 신념을 비트마스크 형태로 저장합니다.
# 민트는 1, 초코는 2, 우유는 4이며, 두 개 이상의 음식은 이들의 비트 OR 연산 결과로 나타납니다.
foodGrid = [[0]*(MAX_SIZE+1) for _ in range(MAX_SIZE+1)]
# faithGrid 배열은 각 칸에 있는 학생의 현재 신앙심을 저장합니다.
faithGrid = [[0]*(MAX_SIZE+1) for _ in range(MAX_SIZE+1)]

# visited 배열은 점심 단계에서 그룹 형성을 위한 DFS 시에 해당 학생(칸)이 방문되었는지를 기록합니다.
visited = [[False]*(MAX_SIZE+1) for _ in range(MAX_SIZE+1)]
# defended 배열은 저녁 전파 단계에서 전파로 인해 방어 상태가 된 칸을 표시하기 위해 사용합니다.
defended = [[False]*(MAX_SIZE+1) for _ in range(MAX_SIZE+1)]

# leaderList 벡터는 점심 단계에서 형성된 각 그룹의 대표자(리더) 정보를 저장합니다.
# 각 요소는 pair로, 첫 번째 부분은 {기본 음식 개수, -대표자 신앙심}이고, 두 번째는 {행 번호, 열 번호}입니다.
# 이 구조는 대표자들을 정렬할 때 신앙심이 높은 순(음수이므로 낮은 값), 그 후 행 번호, 열 번호 순으로 정렬할 수 있게 도와줍니다.
leaderList = []
# groupMembers 벡터는 DFS로 한 그룹을 탐색하는 동안 해당 그룹의 구성원 정보를 임시로 저장하는 벡터입니다.
# 각 원소는 { -신앙심, {행 번호, 열 번호} } 형태로 저장되며, 신앙심을 음수로 저장하는 이유는 내림차순 정렬을 쉽게 하기 위함입니다.
groupMembers = []
# currentGroupSize 변수는 DFS로 탐색할 때 현재 그룹에 속한 학생의 수를 저장합니다.
currentGroupSize = 0

# 함수 isOutOfBounds는 주어진 (row, col)이 격자 범위 밖인지 판별합니다.
# 만약 row나 col이 1보다 작거나 gridSize보다 크면, 격자 범위 밖임을 의미합니다.
def isOutOfBounds(row, col):
    return row < 1 or row > gridSize or col < 1 or col > gridSize

# 함수 countBasicFoods는 주어진 foodValue (비트마스크)에서 기본 음식의 개수를 센 후 반환합니다.
# 여기서 기본 음식은 민트, 초코, 우유이며, 각각 1, 2, 4로 표현됩니다.
def countBasicFoods(foodValue):
    count = 0
    if foodValue & 1:
        count += 1  # 민트가 포함되어 있으면 count 1 증가
    if foodValue & 2:
        count += 1  # 초코가 포함되어 있으면 count 1 증가
    if foodValue & 4:
        count += 1  # 우유가 포함되어 있으면 count 1 증가
    return count

# 함수 dfsGroup는 DFS(깊이 우선 탐색)를 이용해 현재 위치 (row, col)를 시작으로 인접 (상,하,좌,우) 하면서
# 음식 신념이 targetFood와 동일한 학생들을 모두 탐색하여 한 그룹으로 묶습니다.
# 이 함수는 그룹 구성원을 groupMembers 벡터에 저장하고, currentGroupSize를 증가시킵니다.
def dfsGroup(row, col, targetFood):
    global currentGroupSize
    # 현재 (row, col) 위치를 방문한 것으로 표시합니다.
    visited[row][col] = True
    # 그룹 크기를 1 증가시킵니다.
    currentGroupSize += 1
    # 현재 학생의 신앙심을 음수로 변환하여 groupMembers 벡터에 추가합니다.
    groupMembers.append( (-faithGrid[row][col], (row, col)) )
    
    # 4방향에 대해 DFS를 수행합니다.
    for dir in range(DIR_COUNT):
        newRow = row + dx[dir]  # 새로운 행 좌표를 계산합니다.
        newCol = col + dy[dir]  # 새로운 열 좌표를 계산합니다.
        # 새로운 좌표가 격자 범위를 벗어나면 다음 방향으로 넘어갑니다.
        if isOutOfBounds(newRow, newCol):
            continue
        # 이미 방문한 칸이면 다음 방향으로 넘어갑니다.
        if visited[newRow][newCol]:
            continue
        # 만약 새로운 칸의 음식 신념이 targetFood와 다르면 탐색하지 않습니다.
        if foodGrid[newRow][newCol] != targetFood:
            continue
        # 조건을 만족하면 해당 칸을 시작으로 DFS를 재귀적으로 수행합니다.
        dfsGroup(newRow, newCol, targetFood)

# 함수 performLunchPhase는 점심 시간에 진행되는 그룹 형성과 대표자 신앙심 조정 과정을 수행합니다.
# 이 함수는 격자의 각 칸을 검사하여 아직 방문하지 않은 학생에 대해 DFS를 수행해 그룹을 만들고,
# 그룹 내에서 대표자를 결정한 후 대표자에게 그룹원의 신앙심을 전송합니다.
# 또한, 대표자 정보는 evening 단계의 전파를 위해 leaderList 벡터에 저장됩니다.
def performLunchPhase():
    global groupMembers, currentGroupSize, leaderList
    # leaderList 벡터를 초기화합니다.
    leaderList = []
    # 격자 전체에 대해 visited 배열을 false로 초기화합니다.
    for i in range(1, gridSize+1):
        for j in range(1, gridSize+1):
            visited[i][j] = False
    
    # 격자의 모든 칸을 순회하면서 아직 방문하지 않은 칸에 대해 그룹를 형성합니다.
    for i in range(1, gridSize+1):
        for j in range(1, gridSize+1):
            # 만약 해당 칸이 이미 방문되었다면 건너뜁니다.
            if visited[i][j]:
                continue
            # groupMembers 벡터를 초기화합니다.
            groupMembers.clear()
            # 현재 그룹의 크기를 0으로 초기화합니다.
            currentGroupSize = 0
            # 현재 칸의 음식 신념 값을 저장합니다.
            currentFood = foodGrid[i][j]
            # DFS를 통해 해당 칸과 인접하며 음식 신념이 같은 학생들을 그룹으로 묶습니다.
            dfsGroup(i, j, currentFood)
            
            # 그룹 구성원들을 정렬하여 대표자를 결정합니다.
            # 정렬 기준은 음수로 저장된 신앙심 (즉, 실제 신앙심은 내림차순) + 행 번호와 열 번호 순입니다.
            groupMembers.sort()
            # 정렬 후 가장 첫 번째 요소가 대표자가 됩니다.
            leaderRow = groupMembers[0][1][0]
            leaderCol = groupMembers[0][1][1]
            
            # 그룹 대표자에게 그룹의 크기만큼 신앙심을 추가합니다.
            faithGrid[leaderRow][leaderCol] += currentGroupSize
            
            # 대표자의 음식 신념에 포함된 기본 음식의 개수를 계산합니다.
            basicFoodCount = countBasicFoods(foodGrid[i][j])
            
            # 대표자 정보를 leaderList 벡터에 저장합니다.
            # 저장하는 정보는 { {기본 음식 개수, -대표자 신앙심}, {행 번호, 열 번호} } 입니다.
            # 이렇게 저장하면 후속 전파 단계에서 대표자들을 정렬할 때 올바른 순서로 정렬할 수 있습니다.
            leaderList.append( ((basicFoodCount, -faithGrid[leaderRow][leaderCol]), (leaderRow, leaderCol)) )

# 함수 performEveningPropagation는 저녁 시간에 진행되는 대표자의 전파 과정을 수행합니다.
# 각 그룹의 대표자는 정해진 순서에 따라 자신의 신념을 주변 학생들에게 전파합니다.
# 전파는 대표자의 신앙심에 기반하여 방향을 결정하고, 강한 전파와 약한 전파의 조건에 따라 수행됩니다.
def performEveningPropagation():
    # 전파가 시작되기 전에 격자 전체의 defended 배열을 false로 초기화하여 방어 상태가 아닌 상태로 만듭니다.
    for i in range(1, gridSize+1):
        for j in range(1, gridSize+1):
            defended[i][j] = False
    
    # leaderList 벡터를 정렬합니다.
    # 정렬 기준은 먼저 기본 음식 개수가 작은 순, 그 다음 -faith (즉 신앙심이 큰 순), 이후 행 번호, 열 번호 순입니다.
    leaderList.sort()
    
    # 정렬된 leaderList를 순차적으로 처리합니다.
    for idx in range(len(leaderList)):
        # 현재 대표자의 행과 열 좌표를 가져옵니다.
        leaderRow = leaderList[idx][1][0]
        leaderCol = leaderList[idx][1][1]
        # 만약 현재 대표자가 이미 방어 상태라면 전파를 진행하지 않고 넘어갑니다.
        if defended[leaderRow][leaderCol]:
            continue
        
        # 대표자가 전파할 방향을 결정합니다.
        # 전파 방향은 대표자의 현재 신앙심을 4로 나눈 나머지에 따라 결정됩니다.
        propagationDir = faithGrid[leaderRow][leaderCol] % 4
        # 전파 시작점을 대표자의 위치로 초기화합니다.
        currentRow = leaderRow
        currentCol = leaderCol
        
        # 전파 과정에서 대표자가 사용할 전파력 x는 (신앙심 - 1)로 설정됩니다.
        # 전파를 완료한 후 대표자의 신앙심은 1로 재설정합니다.
        remainingPropagationPower = faithGrid[leaderRow][leaderCol] - 1
        faithGrid[leaderRow][leaderCol] = 1
        
        # 대표자는 선택된 방향으로 한 칸씩 이동하며 전파를 진행합니다.
        while True:
            # 다음 칸으로 이동합니다.
            currentRow += dx[propagationDir]
            currentCol += dy[propagationDir]
            # 만약 이동한 칸이 격자 범위를 벗어나면 전파를 종료합니다.
            if isOutOfBounds(currentRow, currentCol):
                break
            # 만약 전파 대상 학생의 음식 신념이 이미 대표자의 음식 신념과 동일하다면 전파를 시도하지 않고 계속 진행합니다.
            if foodGrid[currentRow][currentCol] == foodGrid[leaderRow][leaderCol]:
                continue
            
            # 현재 전파 대상 학생의 신앙심을 targetFaith에 저장합니다.
            targetFaith = faithGrid[currentRow][currentCol]
            # 전파력 (remainingPropagationPower)이 대상 학생의 신앙심보다 큰 경우, 강한 전파가 성공합니다.
            if remainingPropagationPower > targetFaith:
                # 대상 학생의 신앙심을 1 증가시킵니다.
                faithGrid[currentRow][currentCol] += 1
                # 전파력에서 대상 학생의 신앙심 + 1 만큼 감소시킵니다.
                remainingPropagationPower -= (targetFaith + 1)
                # 강한 전파의 경우, 대상 학생의 음식 신념은 대표자의 음식 신념으로 변경됩니다.
                foodGrid[currentRow][currentCol] = foodGrid[leaderRow][leaderCol]
                # 대상 학생은 전파를 받아 방어 상태가 되었음을 표시합니다.
                defended[currentRow][currentCol] = True
            # 만약 전파력 (remainingPropagationPower)이 대상 학생의 신앙심 이하인 경우, 약한 전파가 성공합니다.
            else:
                # 약한 전파에 성공하면 대상 학생의 신앙심은 남은 전파력만큼 증가합니다.
                faithGrid[currentRow][currentCol] += remainingPropagationPower
                # 대상 학생의 음식 신념은 현재 신념과 대표자의 신념의 비트 OR 결과로 변경되어,
                # 기존에 관심 가지던 기본 음식과 대표자가 관심 가지고 있는 기본 음식이 모두 포함됩니다.
                foodGrid[currentRow][currentCol] |= foodGrid[leaderRow][leaderCol]
                # 전파력은 모두 소모되었으므로 0으로 설정합니다.
                remainingPropagationPower = 0
                # 약한 전파에 성공한 대상 학생은 방어 상태가 되었음을 표시합니다.
                defended[currentRow][currentCol] = True
            # 만약 전파력이 0이 되면 전파를 종료합니다.
            if remainingPropagationPower == 0:
                break

# 함수 computeAndPrintDailyAnswer는 하루가 끝난 후 각 음식 종류별 총 신앙심의 합을 계산하고 출력합니다.
# 음식 종류의 출력 순서는 민트초코우유, 민트초코, 민트우유, 초코우유, 우유, 초코, 민트 순입니다.
# 각각의 음식 신념은 비트마스크 값으로 다음과 같이 표현됩니다:
# 민트초코우유: 7 (1|2|4), 민트초코: 3 (1|2), 민트우유: 5 (1|4), 초코우유: 6 (2|4),
# 우유: 4, 초코: 2, 민트: 1.
def computeAndPrintDailyAnswer():
    # faithSums 배열은 인덱스 1부터 7까지 각 비트마스크 값에 해당하는 총 신앙심의 합을 저장합니다.
    faithSums = [0] * 10  # 0번 인덱스는 사용하지 않습니다.
    # 격자 전체를 순회하며 각 칸의 음식 신념에 해당하는 신앙심을 합산합니다.
    for i in range(1, gridSize+1):
        for j in range(1, gridSize+1):
            faithSums[ foodGrid[i][j] ] += faithGrid[i][j]
    # 결과를 지정된 순서대로 출력합니다.
    print(faithSums[7],     # 민트초코우유 (1|2|4)
          faithSums[3],     # 민트초코 (1|2)
          faithSums[5],     # 민트우유 (1|4)
          faithSums[6],     # 초코우유 (2|4)
          faithSums[4],     # 우유 (4)
          faithSums[2],     # 초코 (2)
          faithSums[1])     # 민트 (1)

# 입출력 속도를 향상시키기 위해 동기화를 해제합니다.
import sys
input = sys.stdin.readline

# 첫 번째 줄에서 격자의 크기와 전체 진행 일수를 입력받습니다.
temp = input().split()
gridSize = int(temp[0])
totalDays = int(temp[1])
    
# 격자의 각 행에 대한 초기 음식 신념 정보를 입력받습니다.
# 1부터 gridSize까지 1-indexed 방식으로 저장하며, 편의를 위해 각 줄 앞에 공백을 추가합니다.
for i in range(1, gridSize+1):
    initialFoodGrid[i] = " " + input().strip()
    # 각 칸에 대해 문자를 읽어 해당하는 비트마스크 값으로 변환합니다.
    for j in range(1, gridSize+1):
        foodChar = initialFoodGrid[i][j]
        # 만약 입력 문자가 'T'이면 민트를 의미하고, 민트는 1로 표현합니다.
        if foodChar == 'T':
            foodGrid[i][j] = 1
        # 만약 입력 문자가 'C'이면 초코를 의미하고, 초코는 2로 표현합니다.
        elif foodChar == 'C':
            foodGrid[i][j] = 2
        # 만약 입력 문자가 'M'이면 우유를 의미하고, 우유는 4로 표현합니다.
        elif foodChar == 'M':
            foodGrid[i][j] = 4
    
# 다음으로 각 학생의 초기 신앙심 정보를 입력받아 faithGrid 배열에 저장합니다.
for i in range(1, gridSize+1):
    temp = list(map(int, input().split()))
    for j in range(1, gridSize+1):
        faithGrid[i][j] = temp[j-1]
    
# 각 일(day)에 대해 하루의 과정을 진행합니다.
for day in range(1, totalDays+1):
    # 점심 시간 단계: 학생들이 그룹을 형성하고 대표자에게 신앙심이 전달됩니다.
    performLunchPhase()
    # 저녁 시간 단계: 각 그룹의 대표자가 자신의 신념을 주변으로 전파합니다.
    performEveningPropagation()
    # 하루의 마지막에 각 음식 신념별 총 신앙심의 합을 계산하고 출력합니다.
    computeAndPrintDailyAnswer()