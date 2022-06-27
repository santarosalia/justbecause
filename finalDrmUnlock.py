import time
import uiautomation as auto
import sys
import datetime
import subprocess


def mouseClickAi(ai):
    el = auto.Control(searchDepth=5, AutomationId=ai).GetPosition()
    auto.MoveTo(el[0], el[1], -1)
    auto.Click(el[0], el[1])


def mouseClickName(name):
    el = auto.Control(searchDepth=5, Name=name).GetPosition()
    auto.MoveTo(el[0], el[1], -1)
    auto.Click(el[0], el[1])


def mouseDoubleClickName(name):
    el = auto.Control(searchDepth=5, Name=name).GetPosition()
    auto.MoveTo(el[0], el[1], -1)
    auto.Control(Name=name).DoubleClick()


def editText(ai, text):
    auto.Control(searchDepth=5, AutomationId=ai).SendKeys(text)
    auto.TextControl()


def mouseClickLct(lct):
    el = auto.Control(searchDepth=5, LocalizedControlType=lct).GetPosition()
    auto.MoveTo(el[0], el[1], -1)
    auto.Click(el[0], el[1])


def editTextSend(name, text):
    auto.Control(searchDepth=5, Name=name).SendKeys(text)


newId = sys.argv[1]
newPw = sys.argv[2]
oldId = sys.argv[3]
oldPw = sys.argv[4]
sys.stdout = open(r'C:\RPA\DRMLOG.txt', 'a')
print(datetime.datetime.now())
print('DRM 해제 시작')
failCount = 0
path = r'C:\Program Files\Fasoo Secure Exchange\WPackagerApp.exe'

process = subprocess.Popen(path)

for i in range(4):
    try:
        print(i+1, '차 시도')
        if(i < 2):
            editText('textId', newId)
            editText('textPassword', newPw)
            mouseClickAi('buttonOK')
            print('성공')
            break
        else:
            editText('207', oldId)
            editText('1015', oldPw)
            mouseClickAi('1')
            print('성공')
            break

    except Exception as e:
        failCount += 1
        print('실패')
        time.sleep(10)

process.kill()
print(datetime.datetime.now())
print('DRM 해제 끝')
sys.stdout.close()
