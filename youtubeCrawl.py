from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from tkinter import *
import os
import threading
import sys
import requests

today = ''


def crawl():

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl')
    driver.maximize_window()
    titles = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    uploaders2 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
    uploaders = []
    views = driver.find_elements(
        By.XPATH, '//*[@id="metadata-line"]/span[1]')

    del titles[0: 16]
    del uploaders2[0:20]
    del views[0: 16]

    for i, v in enumerate(uploaders2):
        if i % 2 == 0:
            uploaders.append(v.text)

    for title, uploader, view, no in zip(titles, uploaders, views, range(0, len(titles))):

        notionInsert(uploader, title.text,
                     view.text.split(' ')[1], str(today), no)
    driver.close()


def stopProcess():
    sys.exit()


def notionInsert(uploader, title, view, date, no):
    url = "https://api.notion.com/v1/pages/"
    payload = {
        "parent": {
            "database_id": "c229224e4628408b8907ca96bf89d680"
        },
        "properties": {
            "조회수": {

                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": view
                        }

                    }
                ]
            },
            "제목": {


                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": title

                        }
                    }
                ]
            },
            "업로더": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                                "content": uploader
                        }
                    }
                ]
            },
            "날짜": {


                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": date

                        }
                    }
                ]
            },
            "순번": {


                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                                "content": str(no)

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
        print(datetime.datetime.now())
        print(e)
    # dope


def exec():
    button['text'] = '실행중'
    global today
    while(True):
        if (today != datetime.date.today()):
            today = datetime.date.today()
            crawl()
        sleep(60*60)


if __name__ == "__main__":
    tk = Tk()
    tk.title("유튜브 크롤링")
    iconPath = os.path.join(os.path.dirname(__file__), 'youtube.ico')
    tk.iconbitmap(iconPath)
    tk.minsize(300, 100)
    thread = threading.Thread(target=exec)
    thread.daemon = True
    button = Button(tk, text='실행', command=thread.start, width=30, height=2)
    button2 = Button(tk, text='종료', command=stopProcess, width=30, height=2)
    button.pack(pady=5)
    button2.pack(pady=5)
    tk.mainloop()
# pyinstaller --noconsole --onefile --icon=youtube.ico --add-data="youtube.ico;." youtubeCrawl.py
