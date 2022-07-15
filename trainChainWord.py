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


wordList = []
for word in wordList:
    notionInsert(word)
