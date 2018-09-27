# -*- coding: utf-8 -*-

import time
import hashlib
import requests
import json

requests.adapters.DEFAULT_RETRIES = 20 # 增加重连次数



#  此处为API请求地址及参数
market_url = "http://api.coinbene.com/v1/market/"
trade_url = "http://api.coinbene.com/v1/trade/"
header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",\
    "Content-Type":"application/json;charset=utf-8","Connection":"keep-alive"}
# header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",\
#    "Content-Type":"application/json;charset=utf-8","Connection":"close"}
#  生成签名sign
def sign(**kwargs):
    """
    将传入的参数生成列表形式，排序后用＆拼接成字符串，用hashbli加密成生sign
    """
    sign_list = []
    for key, value in kwargs.items():
        sign_list.append("{}={}".format(key, value))
    sign_list.sort()
    sign_str = "&".join(sign_list)
    mysecret = sign_str.upper().encode()
    m = hashlib.md5()
    m.update(mysecret)
    return m.hexdigest()

#  生成时间戳
def create_timestamp():
    timestamp = int(round(time.time() * 1000))
    return timestamp

timestamp = create_timestamp()

def http_get_nosign(url):
    return http_request(url, data=None)

def http_post_sign(url,dic):
    mysign = sign(**dic)
    del dic['secret']
    dic['sign'] = mysign
    return http_request(url,data=dic)

def http_request(url, data) :
    if data == None:
        time.sleep(0.5)
        tempget = True
        while tempget:
            try:
                reponse = requests.get(url, headers=header_dict)
                tempget = False
            except:
                print "Web is deny our access request, sleep for a while..."
                time.sleep(5)
                continue
    else:
        time.sleep(0.5)
        temppost = True
        while temppost:
            try:
                reponse = requests.post(url, data=json.dumps(data), headers=header_dict)
                temppost = False
            except:
                print "Web is denying our access request, sleep for a while..."
                time.sleep(15)
                continue
    try:
        if reponse.status_code == 200:
            return json.loads(reponse.text)
        else:
            return None
    except Exception as e:
        print ("http failed : %s" % e)
        return None
