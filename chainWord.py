from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import requests
import random
import xml.etree.ElementTree as et
from tkinter import *
import threading
from tkinter.font import Font

doIdx = 0
dictToken = '12F936116531C58AEA09917E970B9753'
prevWordList = []
word = ''


def inputWord(word):
    global prevWordList
    try:
        url = 'https://krdict.korean.go.kr/api/search?key=' + \
            dictToken + '&part=word&q=' + word

        response = requests.get(url, verify=False)

        tree = et.fromstring(response.text)
        if(word == tree.find('item').find('word').text):
            print("있는 단어")
        else:
            print("없는 단어")
            notice["text"] = "없는 단어 입니다!"
            return

        prevWordList.append(word)
        check = notionCheck(word)
        print('notion 확인 완료')
        if(check[0] == 0):
            notionInsert(word)
            print('notion 작성 완료')
        else:
            notionUpdate(check[2], check[1])
            print('notion 수정 완료')
        notionReturnWordList = notionReturn(word.strip()[-1])
        wordList = []

        for notionWord in notionReturnWordList:
            if(notionWord not in prevWordList):
                wordList.append(notionWord)

        if(len(wordList) > 1):
            i = random.randrange(0, len(wordList))
        elif(len(wordList) == 1):
            i = 0
        else:
            prevWordList = []
            return '반박 불가'
        prevWordList.append(wordList[i])
        return wordList[i]

    except Exception as e:
        print(e)
        print("없는 단어")


def inputWord2(word):
    global prevWordList
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    url = 'https://ko.dict.naver.com/#/main'
    driver.get(url)
    driver.implicitly_wait(10)
    xpath = '//input[@id="ac_input"]'
    driver.find_elements(By.XPATH, xpath)[0].send_keys(word+'\n')
    driver.implicitly_wait(10)
    xpath2 = '//div[@class="component_keyword has-saving-function"]'
    xpath3 = '//strong[@class="highlight"]'
    try:

        word = driver.find_elements(By.XPATH, xpath2+xpath3)[0].text
        print("있는 단어")
        prevWordList.append(word)
        check = notionCheck(word)
        print('notion 확인 완료')
        if(check[0] == 0):
            notionInsert(word)
            print('notion 작성 완료')
        else:
            notionUpdate(check[2], check[1])
            print('notion 수정 완료')
        notionReturnWordList = notionReturn(word.strip()[-1])
        wordList = []

        for notionWord in notionReturnWordList:
            if(notionWord not in prevWordList):
                wordList.append(notionWord)

        if(len(wordList) > 1):
            i = random.randrange(0, len(wordList))
        elif(len(wordList) == 1):
            i = 0
        else:
            prevWordList = []
            return '반박 불가'
        prevWordList.append(wordList[i])
        return wordList[i]

    except Exception as e:
        print(e)
        print("없는 단어")

    driver.close()


def notionCheck(word):
    databaseId = "575a36a00fc94b16b33294410d734b29"
    url = "https://api.notion.com/v1/databases/"+databaseId+"/query"
    payload = {
        "filter": {
            "and": [
                {
                    "property": "WORD",
                    "title": {
                        "equals": word
                    }

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
    result = json.loads(response.text)
    pageId = ''
    inputCount = 0
    if(len(result["results"]) > 0):
        inputCount = result["results"][0]["properties"]["inputCount"]["number"]
        pageId = result["results"][0]["id"]

    return [len(result["results"]), inputCount, pageId]


def notionInsert(word):
    url = "https://api.notion.com/v1/pages/"
    payload = {
        "parent": {
            "database_id": "575a36a00fc94b16b33294410d734b29"
        },
        "properties": {
            "WORD": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                                "content": word
                        }
                    }
                ]
            },
            "inputCount":

                {
                    "type": "number",
                    "number": 1

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


def notionReturn(firstCharacter):
    databaseId = "575a36a00fc94b16b33294410d734b29"
    url = "https://api.notion.com/v1/databases/"+databaseId+"/query"
    payload = {
        "filter": {
            "and": [
                {
                    "property": "WORD",
                    "title": {
                        "starts_with": firstCharacter
                    }

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
    result = json.loads(response.text)
    wordList = []
    for r in result["results"]:
        notionWord = r["properties"]["WORD"]["title"][0]["text"]["content"]
        wordList.append(notionWord)

    return wordList


def notionUpdate(pageId, inputCount):

    url = "https://api.notion.com/v1/pages/"+pageId
    payload = {
        "parent": {
            "database_id": "575a36a00fc94b16b33294410d734b29"
        },
        "properties": {
            "inputCount":

                {
                    "type": "number",
                    "number": inputCount+1

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
        response = requests.patch(url, json=payload, headers=headers)
    except Exception as e:
        print(datetime.now())
        print(e)
    # dope

    return json.loads(response.text)


def gameStart():
    startButton.forget()
    notice.pack()
    userInput.pack()
    inputButton.pack()
    userInput.bind("<Return>", test)
    inputButton.bind("<Button-1>", test)


prevWord = ''


def test(e):
    global prevWord, doIdx, prevWordList, notice
    while(True):
        word = userInput.get()
        userInput.delete(first=0, last=len(userInput.get()))
        doIdx += 1
        if(len(prevWordList) != 0):
            if(word not in prevWordList) and (word.strip()[0] == prevWordList[-1].strip()[-1]) and (len(word) != 1):
                returnWord = inputWord(word)
                notice["text"] = returnWord
                print(returnWord)
                break
            else:
                notice["text"] = "잘못 된 단어 입니다!"
                sleep(1)
                notice["text"] = prevWord
                print('잘못 된 단어')
                print(prevWord)

        else:
            if(len(word) != 1):
                returnWord = inputWord(word)
                notice["text"] = returnWord
                break
            else:
                notice["text"] = "잘못 된 단어 입니다!"
                sleep(1)
                notice["text"] = notice["text"] + prevWord
                print('잘못 된 단어')
                print(prevWord)


if __name__ == "__main__":
    tk = Tk()
    tk.title("끝말잇기")

    # tk.iconbitmap(iconPath)

    tk.minsize(400, 200)

    userInput = Entry(tk, width=30, font=Font(weight="bold", size=20))
    notice = Label(tk, width=30, height=2, font=Font(
        weight="bold", size=20))
    notice["text"] = ''
    startButton = Button(
        tk, text='시작', command=gameStart, width=30, height=4, background='white', fg="purple", border="0", activebackground="pink", font=Font(weight="bold"))
    inputButton = Button(
        tk, text='입력', command='', width=40, height=4, background="#FFEAEA", fg="purple", border="0", activebackground="pink", font=Font(weight="bold"))

    startButton.pack(pady=70)

    tk.mainloop()
