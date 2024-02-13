import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5 import uic

global data
global data_list

data_list = []

form_class = uic.loadUiType("Ui_folder\Main_Menu.ui")[0]

class filedata:
    def __init__(self, name, locate, date, owner, price):
        self.name = name
        self.locate = locate
        self.date = date
        self.owner = owner
        self.price = price

    def searchresult(self, InputText):
        if(InputText in self.name):
            return True
        elif(InputText in self.locate):
            return True
        elif(InputText in self.date):
            return True
        elif(InputText in self.owner):
            return True
        elif(InputText in self.price):
            return True
        else:
            return False

    def delete_data(self, delcount):
        if data_list.index(self) == delcount-1:
            return True
        else:
            return False

    def getItems(self):
        returnString ="-----------------------" + "\n" + "물건의 등록 번호 : [ " + str(data_list.index(self) + 1) +" ]"+ "\n" + "물건 이름: " + self.name + "\n" + "물건 위치 : " + self.locate + "\n"+ "보관 날짜 : "+ self.date + "\n" + "물건 주인 : "+ self.owner + "\n" +"물건 가격 : "+ self.price + "\n" + "-----------------------"
        return returnString


class AddWindow(QDialog):
    def __init__(self, parent):
        super(AddWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Add_Window.ui", self)
        self.show()
        self.EnterBTN.clicked.connect(self.Enter_Func)
        self.QuitBTN.clicked.connect(self.CloseAddWindow)

    def CloseAddWindow(self):
        self.close()

    def Enter_Func(self):
        name = self.NameInput.text()
        locate = self.LocateInput.text()
        date = self.DateInput.text()
        owner = self.OwnerInput.text()
        price = self.PriceInput.text()
        data = filedata(name, locate, date, owner, price)
        data_list.append(data)
        self.close()


class ViewWindow(QDialog):
    def __init__(self, parent):
        super(ViewWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\View_Window.ui", self)
        self.show()
        self.QuitBTN.clicked.connect(self.CloseAddWindow)
        self.Result.append("저장되있는 데이터의 목록입니다.")
        self.appendmaster()

    def CloseAddWindow(self):
        self.close()

    def appendmaster(self):
        for cycleadd in data_list:
            self.Result.append(cycleadd.getItems())

class SearchWindow(QDialog):
    def __init__(self, parent):
        super(SearchWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Search_Window.ui", self)
        self.show()
        self.EnterButton.clicked.connect(self.searchout)

    def searchout(self):
        self.close()
        SearchResultWindow(self, self.SearchInput.text())

    def getSearchItemText(self):
        string = self.SearchInput.text()
        return string

class SearchResultWindow(QDialog):
    def __init__(self, parent, InputText):
        super(SearchResultWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Searchres_Window.ui", self)
        self.show()
        self.keyword.setText(InputText)
        self.QuitButton.clicked.connect(self.CloseSearchResultWindow)

        searchResult = False

        for cyclesearch in data_list:
            if cyclesearch.searchresult(InputText):
                self.SearchResult.append(cyclesearch.getItems())
                searchResult = True
        if searchResult == False:
            self.SearchResult.append("\n")
            self.SearchResult.append("\n")
            self.SearchResult.append("      검색 결과가 없습니다.")

    def CloseSearchResultWindow(self):
        self.close()

class DeleteWindow(QDialog):
    def __init__(self, parent, deleteWinRef):
        super(DeleteWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Delete_Window.ui", self)
        self.show()
        self.deleteWindowRef = deleteWinRef
        self.EnterButton.clicked.connect(self.deletecheck)

    def deletecheck(self):
        self.deleteWindowRef.close()
        delcount = int(self.DeleteInput.text())
        checkResult = False
        for cycledelete in data_list:
            isTrue = cycledelete.delete_data(delcount)
            if isTrue:
                del data_list[delcount - 1]
                checkResult = True
                DeleteResultSuccessWindow(self,self.DeleteInput.text())
                self.close()
        if checkResult == False:
            DeleteResultFailWindow(self,self.DeleteInput.text())
            self.close()

class DeleteResultSuccessWindow(QDialog):
    def __init__(self, parent, DeleteInput):
        super(DeleteResultSuccessWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Deleteres_Success_Window.ui", self)
        self.show()
        self.DelNumber.setText(DeleteInput)


class DeleteResultFailWindow(QDialog):
    def __init__(self, parent, DeleteInput):
        super(DeleteResultFailWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Deleteres_Fail_Window.ui", self)
        self.show()
        self.DelNumber.setText(DeleteInput)

class SaveWindow(QDialog):
    def __init__(self, parent):
        super(SaveWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Save_Window.ui", self)
        self.show()
        f = open("c:/temp/data_db.dat", "wt")
        for data in data_list:
            f.write(data.name + '\n')
            f.write(data.locate + '\n')
            f.write(data.date + '\n')
            f.write(data.owner + '\n')
            f.write(data.price + '\n')
        f.close()

class LoadWindow(QDialog):
    def __init__(self, parent):
        super(LoadWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\Load_Window.ui", self)
        self.show()
        f = open("c:/temp/data_db.dat", "rt")
        lines = f.readlines()
        num = len(lines) / 5
        num = int(num)

        for i in range(num):
            name = lines[5 * i].rstrip('\n')
            locate = lines[5 * i + 1].rstrip('\n')
            date = lines[5 * i + 2].rstrip('\n')
            owner = lines[5 * i + 3].rstrip('\n')
            price = lines[5 * i + 4].rstrip('\n')
            data = filedata(name, locate, date, owner, price)
            data_list.append(data)
        f.close()

class CSVWindow(QDialog):
    def __init__(self, parent):
        super(CSVWindow, self).__init__(parent)
        uic.loadUi("Ui_folder\CSV_Window.ui", self)
        self.show()
        f = open("c:/temp/data_db.csv", "w", newline='')
        wr = csv.writer(f)
        wr.writerow(['물건이름', '물건위치', '보관날짜', '물건주인', '물건가격'])
        for data in data_list:
            wr.writerow([data.name] + [data.locate] + [data.date] + [data.owner] + [data.price])
        f.close()

class MenuWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_button.clicked.connect(self.Add_Func)
        self.view_button.clicked.connect(self.View_Func)
        self.search_button.clicked.connect(self.Search_Func)
        self.delete_button.clicked.connect(self.Delete_Func)
        self.save_button.clicked.connect(self.Save_Func)
        self.load_button.clicked.connect(self.Load_Func)
        self.csv_save.clicked.connect(self.CSV_Func)
        self.exit_button.clicked.connect(self.Exit_Func)


    def Add_Func(self):
        AddWindow(self)

    def View_Func(self):
        ViewWindow(self)

    def Search_Func(self):
        SearchWindow(self)

    def Delete_Func(self):
        ViewWindowReference = ViewWindow(self)
        DeleteWindow(self, ViewWindowReference)

    def Save_Func(self):
        SaveWindow(self)

    def Load_Func(self):
        LoadWindow(self)

    def CSV_Func(self):
        CSVWindow(self)

    def Exit_Func(self):
        print("")
        print("이용해 주셔서 감사합니다.")
        exit()

app = QApplication(sys.argv)
mainWindow = MenuWindow()
mainWindow.show()
app.exec()