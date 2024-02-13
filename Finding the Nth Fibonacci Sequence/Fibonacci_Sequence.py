import timeit

pibo = [0,1]
calcu = int(input("n번째 피보나치 수열 구하기 : "))

start_time = timeit.default_timer() #타이머 시작

for i in range(calcu):
    pibo.append(pibo[i]+pibo[i+1])
print(pibo[calcu])

terminate_time = timeit.default_timer() #타이머 종료

print("%f초 걸렸습니다." % (terminate_time - start_time))


