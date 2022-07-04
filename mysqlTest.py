from functools import partial
import threading
from tkinter import messagebox
import pymysql
from tkinter import *
import os
import threading
import sys

serverIp = '192.168.8.62'
dbUser = ''
dbPass = ''
dbName = 'cjaccount'
iconPath = os.path.join(os.path.dirname(__file__), 'chun.ico')
updatePw = ''
deleteList = []


def dbConn(dbUser, dbPass):
    try:
        conn = pymysql.connect(host=serverIp, user=dbUser,
                               password=dbPass, db=dbName, charset='utf8')
        return conn
    except Exception as e:
        messagebox.showerror('error', 'DB 접속 오류')


def insertAccount(inputChannelEntry, inputIdEntry, inputPwEntry):

    conn = dbConn(dbUser, dbPass)
    cur = conn.cursor()
    inputChannel = '"' + inputChannelEntry.get()+'"'
    inputId = '"' + inputIdEntry.get()+'"'
    inputPw = '"' + inputPwEntry.get()+'"'
    query = 'insert into cj_account values((select nextval("cj_account_seq") from dual),' + \
        inputChannel+',' + inputId+','+inputPw+')'
    print(query)
    cur.execute(query)
    conn.commit()
    conn.close()
    tk3.destroy()

    conn = dbConn(dbUser, dbPass)
    cur = conn.cursor()
    cur.execute("select account_no,channel_name, user_id from cj_account")
    row = cur.fetchall()
    conn.close()
    loadAccountInfo(row)


def changePassword(updatePwEntry, account_no):
    updatePw = '"' + updatePwEntry.get()+'"'
    conn = dbConn(dbUser, dbPass)
    cur = conn.cursor()
    query = "update cj_account set user_pw=" + \
        updatePw + " where account_no=" + account_no

    cur.execute(query)
    result = cur.fetchall()

    conn.commit()
    conn.close()
    tk2.destroy()


def changePasswordWindow(account_no):
    global tk2
    tk2 = Tk()
    tk2.title("비밀번호 변경하기")
    tk2.minsize(300, 100)
    tk2.iconbitmap(iconPath)
    updatePwEntry = Entry(tk2)
    updatePwEntry.pack(pady=5)

    updateButton = Button(tk2, text='변경하기', command=partial(
        changePassword, updatePwEntry,  str(account_no)))
    updateButton.pack(pady=5)
    tk2.mainloop()


def newAccountWindow():
    global tk3
    tk3 = Tk()

    tk3.title('신규 계정 등록')
    tk3.minsize(300, 200)
    tk3.iconbitmap(iconPath)
    labelChannel = Label(tk3, text='채널 명')
    labelId = Label(tk3, text='아이디')
    labelPw = Label(tk3, text='비밀번호')
    inputChannelEntry = Entry(tk3)
    inputIdEntry = Entry(tk3)
    inputPwEntry = Entry(tk3, show='*')

    insertButton = Button(tk3, text='등록', command=partial(
        insertAccount, inputChannelEntry, inputIdEntry, inputPwEntry), height=3, width=5)

    labelChannel.grid(row=0, column=0, pady=5, padx=5)
    inputChannelEntry.grid(row=0, column=1, pady=5, padx=5)
    labelId.grid(row=1, column=0, pady=5, padx=5)
    inputIdEntry.grid(row=1, column=1, pady=5)
    labelPw.grid(row=2, column=0, pady=5, padx=5)
    inputPwEntry.grid(row=2, column=1, pady=5)
    insertButton.grid(row=1, column=2, rowspan=2, padx=1)


def stopProcess():
    sys.exit()


def loadAccountInfo(row):
    global deleteList

    for item in deleteList:
        item.destroy()
    deleteList = []
    for i in range(len(row)):
        infoLabel = Label(tk, text=row[i][1]+' : '+row[i][2])
        changePasswordButton = Button(tk, text='비밀번호 변경', command=partial(
            changePasswordWindow, row[i][0]))
        deleteList.append(infoLabel)
        deleteList.append(changePasswordButton)

        infoLabel.pack(pady=5)

        changePasswordButton.pack(pady=5)

    newAccountButton = Button(
        tk, text='계정등록', command=newAccountWindow, width=30, height=2)
    newAccountButton.pack(pady=5)
    deleteList.append(newAccountButton)
    exitButton = Button(tk, text='종료', command=stopProcess, width=30, height=2)
    exitButton.pack(pady=5)
    deleteList.append(exitButton)


def dbLogin():
    global dbUser, dbPass
    dbUser = dbUserEntry.get()
    dbPass = dbPassEntry.get()
    conn = dbConn(dbUser, dbPass)
    cur = conn.cursor()
    cur.execute("select account_no,channel_name, user_id from cj_account")
    row = cur.fetchall()
    conn.close()

    labelId.destroy()
    labelPw.destroy()
    dbUserEntry.destroy()
    dbPassEntry.destroy()
    loginButton.destroy()
    exitButton.destroy()
    loadAccountInfo(row)


if __name__ == "__main__":

    tk = Tk()
    tk.title("DB")

    tk.iconbitmap(iconPath)

    tk.minsize(300, 100)
    dbUserEntry = Entry(tk)
    dbPassEntry = Entry(tk, show='*')
    loginButton = Button(
        tk, text='로그인', command=dbLogin, width=30, height=2)
    exitButton = Button(tk, text='종료', command=stopProcess, width=30, height=2)
    labelId = Label(tk, text='아이디')
    labelId.grid(row=0, column=0, pady=5)
    dbUserEntry.grid(row=0, column=1, pady=5)
    labelPw = Label(tk, text='비밀번호')
    labelPw.grid(row=1, column=0, pady=5)
    dbPassEntry.grid(row=1, column=1, pady=5)
    loginButton.grid(row=2, column=1, pady=5)
    exitButton.grid(row=3, column=1, pady=5)

    tk.mainloop()


# pyinstaller --noconsole --onefile --icon=chun.ico --add-data="chun.ico;." finalMailNotion.py
