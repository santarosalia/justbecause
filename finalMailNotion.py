from datetime import datetime
import email
from time import sleep
from email.header import decode_header, make_header
import poplib
import requests
from tkinter import *
import threading
import sys
import os
from win10toast import ToastNotifier
recentNo = ''
team = ''
status = ''
processName = ''
errorMsg = ''
toaster = ToastNotifier()
# USER INFORMATION
UserId = 'dhkim@edentns.com'
Password = '1q2w3e4r!'
iconPath = os.path.join(os.path.dirname(__file__), 'chun.ico')
# MAIL SERVER SETTING
Host = 'pop.worksmobile.com'
Port = '995'


def ConnectMailSvr():
    global team, status, processName, errorMsg, recentNo
    mail = poplib.POP3_SSL(Host, Port)
    mail.user(UserId)
    mail.pass_(Password)
    #recentNo = 1076
    recentNo = mail.stat()[0]
    rawData = b'\n'.join(mail.retr(recentNo)[1])
    mail.close()
    msg = email.message_from_bytes(rawData)
    fr = make_header(decode_header(msg.get('From')))
    subject = make_header(decode_header(msg.get('Subject')))
    # print(fr)
    # print(subject)
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = msg.get_payload(decode=True)

    if(str(fr).find('fvrpa@cj.net') != -1 or str(fr).find('fv.rpa@cj.net') != -1):
        strSubject = str(subject)
        try:
            processName = strSubject.split(':')[1]
        except Exception as e:
            processName = strSubject
        decodes = ['euc-kr', 'utf-8']
        for decode in decodes:
            decodeBody = ''
            try:
                decodeBody = body.decode(decode)
                strBody = decodeBody
                break
            except Exception as e:
                strBody = body
        if(strBody.find('성공') != -1):
            status = '성공'
            errorMsg = ''
        elif(strBody.find('확인요청') != -1 or strBody.find('확인 요청') != -1):
            status = '확인요청'
            errorMsg = strBody
        elif(strBody.find('오류') != -1):
            status = '오류'
            errorMsg = strBody
        else:
            status = '완료'
            errorMsg = strBody
        team = 'CJ 푸드빌'
        notionInsert()
        print(datetime.now())
        print('notion 작성 완료')
        toaster.show_toast(strSubject, strBody, iconPath, 5)


def notionInsert():
    global team, status, processName, errorMsg
    url = "https://api.notion.com/v1/pages/"
    payload = {
        "parent": {
            "database_id": "5bea681aa7394a40832fe69514a9327c"
        },
        "properties": {
            "status": {

                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": status
                        }

                    }
                ]
            },
            "processName": {


                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": processName

                        }
                    }
                ]
            },
            "team": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                                "content": team
                        }
                    }
                ]
            },
            "errorMessage": {


                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": errorMsg

                        }
                    }
                ]
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": "Bearer secret_NScBJJvTyZmub9pnuX78tkyJErO8RH142EjPplD7bCG"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(datetime.now())
        print(e)
    # dope


run = True


def stopProcess():
    sys.exit()


def exec():
    button['text'] = '실행중'
    while(run):
        # sys.stdout = open(r'','a')
        try:
            mail = poplib.POP3_SSL(Host, Port)
            mail.user(UserId)
            mail.pass_(Password)

            if(recentNo == mail.stat()[0]):
                mail.close()
                continue

            ConnectMailSvr()
        except Exception as e:
            print(datetime.now())
            print(e)
        # sys.stdout.close()


if __name__ == "__main__":
    mail = poplib.POP3_SSL(Host, Port)
    mail.user(UserId)
    mail.pass_(Password)
    recentNo = mail.stat()[0]

    tk = Tk()
    tk.title("메일 감지")

    tk.iconbitmap(iconPath)

    tk.minsize(300, 100)
    thread = threading.Thread(target=exec)
    thread.daemon = True

    button = Button(tk, text='실행', command=thread.start, width=30, height=2)

    button2 = Button(tk, text='종료', command=stopProcess, width=30, height=2)

    mail.close()

    button.pack(pady=5)
    button2.pack(pady=5)

    tk.mainloop()


# pyinstaller --noconsole --onefile --icon=chun.ico --add-data="chun.ico;." finalMailNotion.py
