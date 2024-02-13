#Required Packages ['OpenCV','Tesseract-OCR','PySide2']
import cv2 as cv
import pytesseract
import re
import sys
import os
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic,QtCore, QtGui, QtWidgets

LIMIT_PX = 512
form_class = uic.loadUiType("ui\main.ui")[0]
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' #Tesseract 설치 시 기본으로 설치되는 곳의 주소

def clickable(widget): #객체 클릭 시(마우스를 눌렀다가 때면[ButtonRelease]) 이벤트 발생시키는 함수 /clickable(self.연결할 객체 이름).connect(self.연결할 함수 이름)
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

def image_processing(): #이미지 전처리 함수
    image_cv = cv.imread(filelocation[0]) #함수에 변수로 값 전달하는 방식으로 file location 값을 전달하면 구문 변환 에러가 나옴. (TypeError: Can't convert object to 'str' for 'filename') 그래서 어쩔수 없이 전역변수로 주소값 전달.
    image_PIL = Image.open(filelocation[0])
    height, width, _ = image_cv.shape

    colors = sorted(image_PIL.getcolors(width*height)) #이미지 내 색상정보 추출 및 정렬 -> 색상이 많이 사용된 순으로 정렬
    background_color = '%02x%02x%02x' % (colors[-1][1][0], colors[-1][1][1], colors[-1][1][2])

    ratio = float(LIMIT_PX) / max(height, width)  #설정된 임계치보다 이미지의 크기가 더 클 경우 Resize
    if LIMIT_PX < height or LIMIT_PX < width:
        height = int(height * ratio)
        width = int(width * ratio)
        image_cv = cv.resize(image_cv, (width, height))

    image_gray = cv.cvtColor(image_cv, cv.COLOR_BGR2GRAY) #이미지 흑백화

    #이미지 임계처리
    if background_color > '777777': #배경 색상이 Color Hex #77777 (Grey) 보다 밝으면
        image_fixed = cv.adaptiveThreshold(image_gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,21,8)
    else: #배경 색상이 Grey 보다 어두우면
        image_fixed = cv.adaptiveThreshold(image_gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,3,0)

    filename = "{}.png".format(os.getpid()) #filename 변수에 'pid값.png' 저장
    cv.imwrite(filename, image_fixed) #글자 프로세싱을 위해 filename 변수 이름을 가진 임계처리된 임시 사진 파일을 생성
    return filename

def confidence(img_to_data): #이미지의 정확도(신뢰도) 계산 함수
    sum = 0
    count = 0
    for x in range(0, img_to_data['conf'].count()): 
        if img_to_data['conf'][x] != -1.0:
            sum += img_to_data['conf'][x]
            count += 1
    return sum / count

class Ext_Error_Window(QDialog): #파일 형식자 관련 오류 창 출력
    def __init__(self, parent):
        super(Ext_Error_Window, self).__init__(parent)
        uic.loadUi("ui\ext_error.ui", self)
        self.show()

class Calc_Error_Window(QDialog): #계산 실패 관련 오류 창 출력
    def __init__(self, parent):
        super(Calc_Error_Window, self).__init__(parent)
        uic.loadUi("ui\calc_error.ui", self)
        self.show()

class File_Error_Window(QDialog): #파일 입력 없음 관련 오류 창 출력
    def __init__(self, parent):
        super(File_Error_Window, self).__init__(parent)
        uic.loadUi("ui\_file_error.ui", self)
        self.show()

class main_window(QMainWindow, form_class): #프로그램 시작 시 나오는 메인 창 출력
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global exp; #최초 실행 후 사진 파일 인식 없이 계산 버튼을 눌렀을때 수식 변수의 공백을 인식해 파일 없음 에러 출력 기능을 사용하기 위한 수식 변수 전역변수 사용

        self.setFixedSize(800, 607) #메인 창의 크기를 w 800, h 607 으로 고정 (확장 또는 축소 불가능)
        self.Input_Image.setScaledContents(True) #이미지를 label의 크기에 맞게 자동으로 조절 / self.객체 이름.setScaledContents(True)
        self.Math_Image.setScaledContents(True)
        self.Board_Image.setScaledContents(True)

        clickable(self.Input_Image).connect(self.fileopen) #Input_Image(QLabel) 클릭 시 fileopen 함수 실행
        self.calculate_button.clicked.connect(self.calculate) #calculate_button(QPushButton) 클릭 시 calculate 함수 실행

        #프로그램 실행 시 GUI 관련 이미지 삽입
        self.Kid_Image.setPixmap(QtGui.QPixmap("ui\img\main_kid.png"));
        self.Input_Image.setPixmap(QtGui.QPixmap("ui\img\_board.png"));
        self.Computer_Image.setPixmap(QtGui.QPixmap("ui\img\main_computer.png"));
        self.Board_Image.setPixmap(QtGui.QPixmap("ui\img\main_board.png"));
        self.Math_Image.setPixmap(QtGui.QPixmap("ui\img\windows.png"));
        exp = ''

    def Ext_Error(self): #파일 형식자 관련 오류 창 출력 함수
        Ext_Error_Window(self)

    def Calc_Error(self): #계산 실패 관련 오류 창 출력 함수
        Calc_Error_Window(self)

    def File_Error(self): #파일 입력 없음 관련 오류 창 출력 함수
        File_Error_Window(self)

    def calculate(self): #계산 함수
            try:
                result = eval(exp) #매개변수로 받은 expression(=식)을 문자열로 받아서, 실행하는 함수
                self.answer_label.setText(str(result)) #answer_label(QLabel)을 문자열 정답(result)값으로 지정
            except: #예외 발생 시 
                if(exp == ''): #1) 만약 사진 파일 읽기를 실패하거나 프로그램을 최초 실행하여 수식 변수에 값이 없을 시
                    self.File_Error() #파일 입력 없음 관련 오류 창 출력
                else: #2) 만약 수식 변수에 값은 있는데 수식 인식이 이상하게 되어 정상적인 계산에 실패하여 구문(Syntax) 오류가 발생 시
                    self.Calc_Error()#계산 실패 관련 오류 창 출력
                    self.answer_label.setText('계산 오류')

    def fileopen(self): #사진 파일 삽입 관련 함수
        global filelocation, exp; #위에서 서술하였듯이 사진 파일 주소 구문 변환 에러와 수식 변수의 공백을 전달하기 위한 전역변수 사용
        filelocation = QtWidgets.QFileDialog.getOpenFileName(self, '계산하실 수식이 적힌 사진 파일을 선택해주세요. [.PNG 파일과 .JPEG 파일만 지원합니다.]') #Windows 파일 탐색기를 사용하여 사진 파일을 선택, filelocation 변수에 전달
        if((".png" or ".jpeg") not in filelocation[0]): #인식한 사진 파일의 주소에 .png 또는 .jpeg 확장자 구문이 감지되지 않을 경우
            #오류 출력 및 결과값 변수 초기화
            self.file_location.setText('오류')
            self.math_label.setText('')
            self.confidence_label.setText('')
            self.answer_label.setText('')
            self.Input_Image.setPixmap(QtGui.QPixmap('ui\img\_board.png'));
            self.Math_Image.setPixmap(QtGui.QPixmap('ui\img\error.png'));
            self.Ext_Error()
            exp = ''
        else:
            self.answer_label.setText('')
            self.file_location.setText(filelocation[0]) #file_location(QLabel)을 주소값(filelocation[0])값으로 지정
            image = cv.imread(filelocation[0])
            image_fixed = image_processing() #이미지 전처리 함수에 OpenCV 패키지 읽기 기능을 사용한 값을 전달
            img_to_str = pytesseract.image_to_string(image_fixed, lang = None, config = 'tessedit_char_whitelist=0123456789+-*xX/() --oem 3 --psm 4')
            img_to_data = pytesseract.image_to_data(image_fixed, output_type='data.frame', lang = None, config = 'tessedit_char_whitelist=0123456789+-*xX/() --oem 3 --psm 4', )

            #상자(square) 경계(Bounding Box)
            h, w, _ = image.shape #image.shape를 이용하여 해당 이미지의 높이, 너비 값을 h, w변수에 전달
            boxes = pytesseract.image_to_boxes(image) #인식 된 문자와 해당 상자 경계를 포함하는 결과를 boxes 변수에 전달
            #이미지에 인식된 글자별 상자 경계를 그리기
            for b in boxes.splitlines():
                b = b.split(' ')
                image = cv.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 1)
            cv.imwrite(image_fixed, image) #글자 프로세싱을 위해 임시로 생성된 이미지 파일에 상자 경계를 덮어쓰기

            self.Input_Image.setPixmap(QtGui.QPixmap(filelocation[0]));
            self.Math_Image.setPixmap(QtGui.QPixmap(image_fixed));

            #정규식을 이용하여 계산 가능한 수식으로 변형
            exp = re.sub(r'[^0-9\+\-\*xX\/\(\)\÷\[\]\{\}\\s]', '', img_to_str) #1) 연산자, 피연산자 외 문자 제거
            exp = re.sub(r'[\[\{]', '(', exp) #2) 열린 대/중괄호를 소괄호로 치환
            exp = re.sub(r'[\]\}]', ')', exp) #3) 닫힌 대/중괄호를 소괄호로 치환
            exp = exp.replace('x', '*')

            conf = confidence(img_to_data)
            conf_string = '{0:0.3f}'.format(conf) #정확도(신뢰도)의 소숫점 값을 3자리까지 잘라서 문자열로 conf_string 변수에 저장

            self.math_label.setText(exp)
            self.confidence_label.setText(conf_string)
            os.remove(image_fixed) #글자 프로세싱을 위해 임시로 생성된 이미지 파일 삭제

app = QApplication(sys.argv)
mainWindow = main_window()
mainWindow.show()
app.exec()