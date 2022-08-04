#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import execjs
from requests.utils import dict_from_cookiejar
def get_ac_sign(ac_nonce):
    with open('_ac_signature.js', 'r', encoding='utf-8') as f:
        b = f.read()
    c = execjs.compile(b)
    d = c.call('get_ac_signature',ac_nonce)
    return d

def run():
    sess = requests.session()
    url = "https://www.douyin.com/user/MS4wLjABAAAA_LnjYFypepqF2YXZysc8Mp-8ln6rid5qe_7OcBdy68I"
    __ac_nonce = dict_from_cookiejar(sess.get(url).cookies)['__ac_nonce']
    __ac_signature = get_ac_sign(__ac_nonce)
    sess.headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en-XA;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'cookie':f'__ac_nonce={__ac_nonce}; __ac_signature={__ac_signature}',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    payload = {}
    response = sess.get(url,  data=payload)
    html = etree.HTML(response.content)
    href = html.xpath('//li[@class="ECMy_Zdt"]/a/@href')
    name = html.xpath('//li[@class="ECMy_Zdt"]/a/div/div/img/@alt')
    print(len(href))
    print(len(name))
    ip_loc = ''.join(html.xpath('//*[contains(text(), "IP属地")]//text()'))
    print(ip_loc)
    return ip_loc


if __name__ == '__main__':
    run()