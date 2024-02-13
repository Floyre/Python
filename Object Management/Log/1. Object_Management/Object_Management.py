data_list = []

class filedata:
    def __init__(self, name, locate, date, owner, price):
        self.name = name
        self.locate = locate
        self.date = date
        self.owner = owner
        self.price = price

    def print_data(self):
        print("-----------------------")
        print("물건의 등록 번호 :",'[', data_list.index(self) + 1,']',"번 입니다.")
        print("물건이름: ", self.name)
        print("물건위치: ", self.locate)
        print("보관날짜: ", self.date)
        print("물건주인: ", self.owner)
        print("물건가격: ", self.price)
        print("-----------------------")

    def searchresult(self, keyword):
        if(keyword in self.name):
            return True
        elif(keyword in self.locate):
            return True
        elif(keyword in self.date):
            return True
        elif(keyword in self.owner):
            return True
        elif(keyword in self.price):
            return True
        else:
            return False

    def delete_data(self, delcount):
        if data_list.index(self) == delcount-1:
            return True
        else:
            return False

def set_data():
    name = input("물건이름: ")
    locate = input("물건위치: ")
    date = input("보관날짜: ")
    owner = input("물건주인 : ")
    price = input("물건가격 : ")
    data = filedata(name, locate, date, owner, price)
    return data

def print_menu():
    print("<메뉴>")
    print("1)등록")
    print("2)조회")
    print("3)검색")
    print("4)삭제")
    print("5)저장")
    print("6)불러오기")
    print("7)정렬")
    print("8)종료")
    answer = int(input("선택하세요 :"))
    return int(answer)


def run():
    while 1:
        answer = print_menu()
        if answer == 1:
            data = set_data()
            data_list.append(data)
        elif answer == 2:
            print_all_data(data_list)
        elif answer == 3:
            keyword = str(input("찾고 싶으신 키워드를 입력해주세요 :"))
            searchcountdown = 0
            for data in data_list:
                if data.searchresult(keyword):
                    data.print_data()
                    searchcountdown += 1
            if searchcountdown == 0:
                print("")
                print("데이터가 없습니다")
                print("")
        elif answer == 4:
            for data in data_list:
                data.print_data()
            delcount = int(input("삭제하실 물건의 등록 번호를 입력해주세요 :"))
            print_all_data(data_list)
            for singleData in data_list:
                isTrue = singleData.delete_data(delcount)

                if isTrue:
                    delcount -= 1
                    del data_list[delcount]
                    delcount += 1
                    print(delcount, '번의 데이터가 정상적으로 삭제되었습니다.')
                    for data in data_list:
                        data.print_data()
                    print("남은 데이터 목록입니다.")
                else:
                    print('해당 항목은 [',delcount,']',"번호가 일치하지 않습니다.")
        elif answer == 5:
            save_data(data_list)
            print("data_db.dat 파일로 저장 완료되었습니다.")
        elif answer == 6:
            load_data(data_list)
            print("data_db.dat 파일 불러오기 완료되었습니다.")
        #elif answer == 7: 취소된 기능
            print("")
            print(" 1 번 | 물건 이름")
            print(" 2 번 | 물건 위치")
            print(" 3 번 | 보관 날짜")
            print(" 4 번 | 물건 주인")
            print(" 5 번 | 물건 가격")
            print("")
            sortmg = int(input("어떤 기준으로 정렬 하시겠습니까 ? : "))

            if sortmg == 1:
                print('1번')
                data.name.sort()
                print(data.name)
            elif sortmg == 2:
                print('2번')
            elif sortmg == 3:
                print('3번')
            elif sortmg == 4:
                print('4번')
            elif sortmg == 5:
                print('5번')

        elif answer == 8:
            break


def print_all_data(data_list):
    for data in data_list:
        data.print_data()

def save_data(data_list):
    f = open("c:/temp/data_db.dat","wt")
    for data in data_list:
        f.write('물건이름: ' + data.name + '\n')
        f.write('물건위치: ' + data.locate + '\n')
        f.write('보관날짜: ' + data.date + '\n')
        f.write('물건주인: ' + data.owner + '\n')
        f.write('물건가격: ' + data.price + '\n')
    f.close()

def load_data(data_list):
    f = open("c:/temp/data_db.dat", "rt")
    lines = f.readlines()
    num = len(lines) / 5
    num = int(num)

    for i in range(num):
        name = lines[5*i].rstrip('\n')
        locate = lines[5*i+1].rstrip('\n')
        date = lines[5*i+2].rstrip('\n')
        owner = lines[5*i+3].rstrip('\n')
        price = lines[5*i+4].rstrip('\n')
        data = filedata(name, locate, date, owner, price)
        data_list.append(data)
    f.close()


if __name__ == "__main__":
    run()
