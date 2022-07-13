from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import requests
import random


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
        print("있는 단어")
        word = driver.find_elements(By.XPATH, xpath2+xpath3)[0].text
        check = notionCheck(word)
        print('notion 확인 완료')
        if(check[0] == 0):
            notionInsert(word, 0)
            print('notion 작성 완료')
        else:
            notionUpdate(word, check[1])
            print('notion 수정 완료')
        wordList = notionReturn(word.strip()[-1])
        if(len(wordList) > 1):
            i = random.randrange(0, len(wordList))
        elif(len(wordList) == 1):
            i = 0
        else:
            return '반박 불가'
        return wordList[i]

    except Exception:
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
    inputCount = 0
    if(len(result["results"]) > 0):
        inputCount = result["results"][0]["properties"]["inputCount"]["rich_text"][0]["number"]["content"]

    return [len(result["results"]), inputCount]


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


def notionUpdate(word, inputCount):


word = input('단어')
while(True):
    returnWord = inputWord(word)
    print(returnWord)
    word = input('단어')
