import requests
import json
import pandas as pd
import html
import re

CLIENT_ID = '3q5CdnaIhuYAlTI0rNRK'
CLIENT_SECRET = '20ZmNFLdPM'
headers = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,
    'Content-Type': 'application/json',
}

def translate(line):
    data = {
        'source': 'ko',
        'target': 'en',
        'text': line
    }
    data_str = json.dumps(data)
    data_str = data_str.replace("&apos;", "'")
    url2 = 'https://openapi.naver.com/v1/papago/n2mt'
    response = requests.post(url2, headers=headers, data=data_str.encode('utf-8'))
    if response.status_code == 200:
        result = response.json().get('message', {}).get('result', {})
        translated_text = result.get('translatedText')
        translated_text = re.sub(r'<\/?b>', '', translated_text)
        return html.unescape(translated_text)
    else:
        return None



def get_news_data(query):
    url = f'https://openapi.naver.com/v1/search/news.json?query={query}&display=10&start=1'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.text)
        return None
    else:
        items = response.json()['items']
        datas = []
        for i in items:
            title = re.sub('<.*?>', '', html.unescape(i['title']))
            description = re.sub('<.*?>', '', html.unescape(i['description']))
            data = {
                'Title': title,
                'PubDate': html.unescape(i['pubDate']),
                'Originallink': html.unescape(i['originallink']),
                'Description': description,
                'Papago': translate(title)
            }
            print(title)
            datas.append(data)
        return pd.DataFrame(datas)

data = get_news_data('경성대')
data.to_csv('translate.csv', index=False)
