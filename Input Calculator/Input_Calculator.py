formula = []

for i in range(3):
    form = str(input("계산할걸 넣으세요 숫자 또는 사칙연산 (+,-,*,/): "))
    formula.append(form)
    print(formula)

plus = '+'
minus = '-'
multiply = '*'
nanugi = '/'

rangform = len(formula)
if plus in formula:
    foundplus = formula.index(plus)
    backgapplus = int(formula[foundplus-1])
    apgapplus = int(formula[foundplus+1])
    print("계산 결과입니다 : ",backgapplus + apgapplus)
elif minus in formula:
    foundminus = formula.index(minus)
    backgapminus = int(formula[foundminus-1])
    apgapminus = int(formula[foundminus+1])
    print("계산 결과입니다 : ",backgapminus - apgapminus)
elif multiply in formula:
    foundmultiply = formula.index(multiply)
    backgapmultiply = int(formula[foundmultiply-1])
    apgapmultiply = int(formula[foundmultiply+1])
    print("계산 결과입니다 : ",backgapmultiply * apgapmultiply)
elif nanugi in formula:
    foundnanugi = formula.index(nanugi)
    backgapnanugi = int(formula[foundnanugi-1])
    apgapnanugi = int(formula[foundnanugi+1])
    print("계산 결과입니다 : ",backgapnanugi / apgapnanugi)