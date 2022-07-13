from datetime import datetime
from time import sleep
import requests
from tkinter import *
import threading
import sys
import os
from win10toast import ToastNotifier
import json
recentNo = ''
team = ''
status = ''
processName = ''
errorMsg = ''
toaster = ToastNotifier()
iconPath = os.path.join(os.path.dirname(__file__), 'chun.ico')


def notionCheck():
    global team, status, processName, errorMsg
    databaseId = "5bea681aa7394a40832fe69514a9327c"
    url = "https://api.notion.com/v1/databases/"+databaseId+"/query"
    payload = {
        "filter": {
            "and": [
                {
                    "property": "title",

                }
            ]
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

    return json.loads(response.text)


run = True


def stopProcess():
    sys.exit()


def exec():
    global recentNo
    button['text'] = '실행중'
    while(run):
        # sys.stdout = open(r'','a')
        try:
            response = notionCheck()
            if(recentNo != response["results"][0]["id"]):
                recentNo = response["results"][0]["id"]
                status = response["results"][0]["properties"]["status"]["rich_text"][0]["text"]["content"]
                processName = response["results"][0]["properties"]["processName"]["rich_text"][0]["text"]["content"]
                toaster.show_toast(processName, status, iconPath, 5)
        except Exception as e:
            print(datetime.now())
            print(e)
        # sys.stdout.close()


if __name__ == "__main__":
    response = notionCheck()
    recentNo = response["results"][0]["id"]

    tk = Tk()
    tk.title("NOTION CHECK")

    tk.iconbitmap(iconPath)

    tk.minsize(300, 100)
    thread = threading.Thread(target=exec)
    thread.daemon = True

    button = Button(tk, text='실행', command=thread.start, width=30, height=2)

    button2 = Button(tk, text='종료', command=stopProcess, width=30, height=2)

    button.pack(pady=5)
    button2.pack(pady=5)

    tk.mainloop()


# pyinstaller --noconsole --onefile --icon=chun.ico --add-data="chun.ico;." finalMailNotion.py
