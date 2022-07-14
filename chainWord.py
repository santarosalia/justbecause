from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import requests
import random

prevWordList = []


def inputWord(word):

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
    inputCount += 1
    url = "https://api.notion.com/v1/pages/"+pageId
    payload = {
        "parent": {
            "database_id": "575a36a00fc94b16b33294410d734b29"
        },
        "properties": {
            "inputCount":

                {
                    "type": "number",
                    "number": inputCount

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

    return json.loads(response.text)


word = input('단어')
while(True):
    returnWord = inputWord(word)
    print(returnWord)
    while(True):
        word = input('단어')
        if(word not in prevWordList):
            break
        else:
            print('중복!')
            continue
