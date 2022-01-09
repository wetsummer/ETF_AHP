import pandas, numpy, datetime, calendar, os, glob, random, multiprocessing, threading, math, time

def return_val_date(table, year, month, day=1, way='go', deep=0): #가장 근처 거래일 찾기(입력: 거래 자료, 기준년, 기준 월, 기준일, 방향(go: 미래로, back: 과거로), 재귀 깊이)
    if deep > 20:
        return numpy.nan, numpy.nan, numpy.nan
    deep += 1

    try:
        table['Close'][str(year) + '-' + str(month) + '-' + str(day)]
    except:
        if way == 'go':
            (year, month, day) = return_val_date(table, year, month, day+1, way, deep)
        elif way == 'back':
            (year, month, day) = return_val_date(table, year, month, day-1, way, deep)
        else:
            print('ERROR!')

    return year, month, day

def AHP(A, way='big'): #선호도 분석(입력: 변동 표, 방법(big: 큰 것 선호, small: 작은 것 선호))
    A = A.reshape(-1)
    length = len(A)
    ahp_table = numpy.empty(shape=(length, length))
    interval = (numpy.max(A) - numpy.min(A))/9
    if way == 'big':
        for x in range(length):
            for y in range(length):
                if A[x] >= A[y]:
                    if A[x] - A[y] <= interval:
                        ahp_table[x][y] = 1
                    elif A[x] - A[y] <= interval * 2:
                        ahp_table[x][y] = 2
                    elif A[x] - A[y] <= interval * 3:
                        ahp_table[x][y] = 3
                    elif A[x] - A[y] <= interval * 4:
                        ahp_table[x][y] = 4
                    elif A[x] - A[y] <= interval * 5:
                        ahp_table[x][y] = 5
                    elif A[x] - A[y] <= interval * 6:
                        ahp_table[x][y] = 6
                    elif A[x] - A[y] <= interval * 7:
                        ahp_table[x][y] = 7
                    elif A[x] - A[y] <= interval * 8:
                        ahp_table[x][y] = 8
                    elif A[x] - A[y] <= interval * 9:
                        ahp_table[x][y] = 9
                    else:
                        ahp_table[x][y] = 9
                elif A[x] < A[y]:
                    if A[x] - A[y] >= -interval:
                        ahp_table[x][y] = 1
                    elif A[x] - A[y] >= -interval * 2:
                        ahp_table[x][y] = 1/2
                    elif A[x] - A[y] >= -interval * 3:
                        ahp_table[x][y] = 1/3
                    elif A[x] - A[y] >= -interval * 4:
                        ahp_table[x][y] = 1/4
                    elif A[x] - A[y] >= -interval * 5:
                        ahp_table[x][y] = 1/5
                    elif A[x] - A[y] >= -interval * 6:
                        ahp_table[x][y] = 1/6
                    elif A[x] - A[y] >= -interval * 7:
                        ahp_table[x][y] = 1/7
                    elif A[x] - A[y] >= -interval * 8:
                        ahp_table[x][y] = 1/8
                    elif A[x] - A[y] >= -interval * 9:
                        ahp_table[x][y] = 1/9
                    else:
                        ahp_table[x][y] = 1/9
    elif way == 'small':
        for x in range(length):
            for y in range(length):
                if A[x] >= A[y]:
                    if A[x] - A[y] <= interval:
                        ahp_table[x][y] = 1
                    elif A[x] - A[y] <= interval * 2:
                        ahp_table[x][y] = 1/2
                    elif A[x] - A[y] <= interval * 3:
                        ahp_table[x][y] = 1/3
                    elif A[x] - A[y] <= interval * 4:
                        ahp_table[x][y] = 1/4
                    elif A[x] - A[y] <= interval * 5:
                        ahp_table[x][y] = 1/5
                    elif A[x] - A[y] <= interval * 6:
                        ahp_table[x][y] = 1/6
                    elif A[x] - A[y] <= interval * 7:
                        ahp_table[x][y] = 1/7
                    elif A[x] - A[y] <= interval * 8:
                        ahp_table[x][y] = 1/8
                    elif A[x] - A[y] <= interval * 9:
                        ahp_table[x][y] = 1/9
                    else:
                        ahp_table[x][y] = 1/9
                elif A[x] < A[y]:
                    if A[x] - A[y] >= -interval:
                        ahp_table[x][y] = 1
                    elif A[x] - A[y] >= -interval * 2:
                        ahp_table[x][y] = 2
                    elif A[x] - A[y] >= -interval * 3:
                        ahp_table[x][y] = 3
                    elif A[x] - A[y] >= -interval * 4:
                        ahp_table[x][y] = 4
                    elif A[x] - A[y] >= -interval * 5:
                        ahp_table[x][y] = 5
                    elif A[x] - A[y] >= -interval * 6:
                        ahp_table[x][y] = 6
                    elif A[x] - A[y] >= -interval * 7:
                        ahp_table[x][y] = 7
                    elif A[x] - A[y] >= -interval * 8:
                        ahp_table[x][y] = 8
                    elif A[x] - A[y] >= -interval * 9:
                        ahp_table[x][y] = 9
                    else:
                        ahp_table[x][y] = 9
    else:
        print('Error!')

    return ahp_table
        
def AHP_score(A): #점수 얻기(입력: 선호도 표)
    row = len(A)
    A = numpy.array(A)
    B = numpy.empty(shape=(row, row))
    A_sum = A.sum(axis=0)
    smallest = get_smallest_num_biggrt_then_zero()
    A_sum = numpy.where(A_sum == 0, smallest, A_sum)
    for a in range(row):
        for b in range(row):
            B[a,b] = A[a,b]/A.sum(axis=0)[b]

    # 점수
    score = numpy.empty(row)
    for x in range(row):
        score[x] = numpy.average(B[x])

    return score

def get_smallest_num_biggrt_then_zero(): #0보다 큰 가장 작은 양수. 0으로 나누기 방지용
    smallest= 1
    th = 0
    while smallest != 0:
        smallest /= 10
        th += 1
    
    smallest= 1
    for i in range(th - 1):
        smallest /= 10

    return smallest

def AHP_const(A, score): #일관성 척도 얻기(입력: 선호도 표, 점수표)
    row = len(A)
    A = numpy.array(A)
    const_index = numpy.empty(row)
    for x in range(row):
        const_index[x] = numpy.sum(score*A[x])/score[x]

    return const_index

def AHP_const_index(A): #일관성 지수 얻기(입력: 일관성 척도)
    A = numpy.array(A)
    return (numpy.average(A)-len(A))/(len(A)-1)

def AHP_const_ratio(ci, ri): #일관성 비율 얻기(입력: 일관성 지수, 무작위 일관성 지수)
    return ci/ri

def AHP_RI(n): #무작위 일관성 지수 획득(입력: 대안 개수)
    cpu = os.cpu_count()
    #num =  math.ceil(10000/cpu/2)*n
    num = 1000
    sqrt_n = 1 #표본 개수의 제곱근
    z = 2.58 #신뢰구간 99%의 z값
    x = 0
    x_tmp = []
    var = []
    sigma = 0
    chk = True
    samples = []
    while (round(x+(z*(sigma/sqrt_n)), 2) != round(x-(z*(sigma/sqrt_n)), 2)) or chk:
        sd = round(random.random() * 100000000000000)
        samples += AHP_random_const_index(n, num, cpu, sd)
        #print(len(samples))
        sqrt_n = math.sqrt(len(samples))
        x_tmp.append(samples)
        x = numpy.average(x_tmp) #표본 평균
        var.append(samples) #표본 분산
        sigma = numpy.sqrt(numpy.average(var)) #표본 표준편차
        chk = False
        #print("신뢰구간 상한: {0} 신뢰구간 하한: {1}".format(x+(z*(sigma/sqrt_n)), x-(z*(sigma/sqrt_n))))

    return x

def AHP_random_const_index(n, num, cpu, sd): #무작위 일관성 지수 획득(입력: 대안 개수, 작업 당 처리할 표본 개수, 난수 씨앗)
    cpu = cpu * 4 #다중처리 개수
    mt = [None] * cpu
    mt_result = [None] * cpu
    for i in range(cpu):
        mt[i] = threading.Thread(target=AHP_random_const_index_inside, args=(n, num, sd, i, mt_result), daemon = True)
        mt[i].start()
    
    for i in range(cpu):
        mt[i].join()
    
    #save = numpy.sum(mt_result)
    save = numpy.array(mt_result, dtype=numpy.float64).reshape(-1).tolist()
    #print(ran)
    #return save/num
    return save

def AHP_random_const_index_inside(n, num, sd, ind, result): #무작위 일관성 지수 계산(입력: 대안 개수, 계산할 개수, 난수 씨앗, 병렬처리 번호, 결과 저장 변수)
    save = []
    possible = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1/1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 1/9]
    random.seed(sd)

    for i in range(num):
        maxt = numpy.zeros(shape=(n,n))
        ran = random.choices(possible, k = int(((n*n-n)/2)))
        th = 0
        for x in range(n):
            maxt[x,x] = 1
            for y in range(n):
                if maxt[y,x] == 0:
                    if y > x:
                        maxt[y,x] = ran[th]
                        th += 1
                    else:
                        maxt[y,x] = 1/maxt[x,y]
        #save += AHP_const_index(AHP_const(maxt, AHP_score(maxt)))
        save.append(AHP_const_index(AHP_const(maxt, AHP_score(maxt))))
        #print(i)

    result[ind] = save

if __name__=="__main__":
    print(AHP_RI(8)) #표본, 표본 개수 반환
    '''a = numpy.array([[1,1/5,1/9,1],[5,1,1,5],[9,1,1,5],[1,1/5,1/5,1]])
    a = AHP_const_ratio(AHP_const_index(AHP_const(a, AHP_score(a))), 0.9)
    print(a)'''
