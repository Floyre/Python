import os
 
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("")
        print ('에러,' +  directory + '에 폴더 생성을 실패했습니다.')
        print("")

while True:
    print("")
    print('폴더를 생성할 타입을 선택해주세요.')
    print("")
    print("[1] 일반 폴더 생성")
    print("[2] 반복 폴더 생성")
    print("[3] 종료")
    typeques = input("입력 : ")
    
    if typeques == '1':
        print("")
        print("*일반 폴더 생성 모드가 선택되었습니다.*")
        print("*취소를 원하신다면 폴더 제목에 취소를 입력해주세요.*")
        print("")
        while True:
            address = input("폴더를 생성할 위치를 입력해주세요 : ")
            name = input("폴더 제목을 입력해주세요 : ")
            if (name == '취소'):
                print("")
                print("취소되었습니다.")
                print("")
                break
            else:
                print("")
                print("-다음 정보가 맞는지 확인 부탁드립니다.-")
                print("1.폴더를 생성할 위치 : " , address)
                print("2.폴더 제목 : " , name )
                print("")
                answer = input("맞다면 예, 틀린 정보가 있다면 아니오 를 입력해주세요. : ")
                if answer == '예':
                    createFolder(address + '/' + name)
                    print("")
                    print('요청하신 폴더' , name , '폴더가 성공적으로 생성되었습니다.')
                    print("")
                    break
                else:
                    continue


    elif typeques == '2':
        print("")
        print("*반복 폴더 생성 모드가 선택되었습니다.*")
        print("*취소를 원하신다면 숫자 뒤에 올 문장에 취소를 입력해주세요.*")
        print("")
        while True:
            address = input("폴더를 생성할 위치를 입력해주세요 : ")
            countstart = int(input("생성할 폴더 개수의 시작점 ? (숫자만 입력해주세요) : "))
            countend = int(input("생성할 폴더 개수의 종료지점 ? (숫자만 입력해주세요) : "))
            name = input("숫자 뒤에 올 문장을 입력해주세요 : ")
            counter = 0

            if (name == '취소'):
                print("")
                print("취소되었습니다.")
                print("")
                break
            else:
                for i in range (countstart,countend+1):
                    counter +=1
                print("")
                print("- 다음 정보가 맞는지 확인 부탁드립니다.-")
                print("1.폴더를 생성할 위치 : " , address)
                print("2.폴더를 생성할 개수 : " , counter)
                print("3.폴더를 생성할 배열 : " , countstart , "~" , countend)
                print("4.폴더 제목 : " , str(countstart) , "~" , str(countend) + name )
                print("")
                answer = input("맞다면 예, 틀린 정보가 있다면 아니오 를 입력해주세요. : ")
                if answer == '예':
                    for i in range (countstart,countend+1):
                        createFolder(address + '/' + str(i)+ name)
                    print("")
                    print('요청하신 폴더' , counter , '개가 성공적으로 생성되었습니다.')
                    print("")
                    break
                else:
                    continue
    elif typeques == '3':
        print("")
        print("이용해주셔서 감사합니다.")
        print("")
        break
    else:
        print("")
        print("잘못된 입력입니다.")
        print("")
        continue
