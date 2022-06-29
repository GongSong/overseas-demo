import requests
import time
from tqdm import tqdm
import pandas as pd
import numpy as np
import re


#这里可能也要修改
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "authorization": "OTU4MTk3NzMzNTY5NzQ5MDAy.YkJ2Ag.E4RT0ALuuyWr1Ytc_TN_0G4KPuE",
    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InpoLUNOIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDAuMC40ODk2LjEyNyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAuNDg5Ni4xMjciLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20uaGsvIiwicmVmZXJyaW5nX2RvbWFpbiI6Ind3dy5nb29nbGUuY29tLmhrIiwic2VhcmNoX2VuZ2luZSI6Imdvb2dsZSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMzMzNzcsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9",
    "cookie": "__dcfduid=33e576e0af0b11ecacf421044cb0b85c; __sdcfduid=33e576e1af0b11ecacf421044cb0b85c3b11a81671047def08f144a9c4fea5e370d50311a16a60c0a9b852455c597243; _ga=GA1.2.746746656.1648522323; _gid=GA1.2.316747310.1656300180; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+27+2022+11%3A23%3A11+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __cf_bm=VMwcAKsDzplxGncRgenbDzkCy15KAXG0.MIxwR3I9MQ-1656313275-0-AY3YHcwAdWfZ+eFjMum8idZ2Am4beP2/roIdJ0MwtS857dWt8HrJWpSLmimagPr695UswkA+/ex3SV9ziAgjXoFdILi/NwZEiX1AzfyDiygw8bpBhYB8pXdzlwC4qY5IwA==",
}


def check_status(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        content = html.json()
        messages = content['total_results']
        return messages
    else:
        print(html.status_code)


def get_html():
    number = int(total / 25) +1
    list_number = [(j * 25) for j in range(0,number+1)]
    for i in [tqdm(list_number)]:
        href = url + "&offset={}".format(i)
        html = requests.get(url=href, headers=headers)
        content = html.json()
        messages = content['messages']
        for m in messages:
            try:
                comment = m[0]['content'].strip('\n\n').replace('\n','')
            except:
                comment = np.NAN
            try:
                timedeate = m[0]['timestamp']
            except:
                timedeate = np.NAN

            if len(comment) != 0:
                strinfo = re.compile('\<.*?\>')
                comment1 = strinfo.sub(' ', comment)
            df = pd.DataFrame()
            df['发文时间'] = [timedeate]
            df['内容信息'] = [comment1]
            df.to_csv('./input/原始数据.csv', mode='a+', header=None, index=None)
        time.sleep(1)


if __name__ == '__main__':
    #这里是要修改的
    url = 'https://discord.com/api/v9/guilds/494953173954592769/messages/search?min_id=987386137804800000&max_id=989560464998400000'
    total = check_status(url)
    df = pd.DataFrame()
    df['发文时间'] = ['发文时间']
    df['内容信息'] = ['内容信息']
    df.to_csv('./input/原始数据.csv',mode='w',header=None,index=None)
    get_html()
