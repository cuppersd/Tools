

#https://www.amazon.co.jp/s/ref=sr_pg_2?fst=as%3Aon&rh=n%3A52374051%2Cn%3A5267102051%2Cn%3A169667011%2Ck%3A%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&page=2&keywords=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&ie=UTF8&qid=1546071162
#https://www.amazon.co.jp/s/ref=sr_pg_3?fst=as%3Aon&rh=n%3A52374051%2Cn%3A5267102051%2Cn%3A169667011%2Ck%3A%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&page=3&keywords=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&ie=UTF8&qid=1546071226
#https://www.amazon.co.jp/s/ref=sr_pg_4?fst=as%3Aon&rh=n%3A52374051%2Cn%3A5267102051%2Cn%3A169667011%2Ck%3A%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&page=4&keywords=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&ie=UTF8&qid=1546071269

import re
import requests
import sys
import uuid
import urllib.request
from bs4 import BeautifulSoup
import time
import random
 
pattern = r'<a class="a-size-small a-link-normal a-text-normal" href="(.*?)"'
regex = re.compile(pattern)
 
 
def Get_Images(URL,f):
    """
    A function that returns all image URLs found within a given website
    """
    user_agent=[
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    ]

    headers={
    'User-Agent':random.choice(user_agent),
    'Connection':'keep-alive',
    'GET':URL,
    'Host':'www.amazon.co.jp',
    }
 
    print("\nAttempting to download images from the given URL.\n")
    r = requests.get(URL,headers=headers)
 
    if r.status_code != 200:
        print("Error retrieving the desired website. Aborting! Try again later.\n\n")
        sys.exit(1)
    elif r.status_code == 200:
        html = r.text
  
        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.select('a')
        new_url_img=[]
        for x in item_list:
            All_Images = re.findall(regex, str(x))
            if len(All_Images)!=0:
                if 'https://www.amazon.co.jp/gp/' not in All_Images[0]:
                    new_url_img.append(All_Images[0])
        print(len(set(new_url_img)))
        for each_item in set(new_url_img):
        	f.write(each_item+'\n')






        

 
    return None
 
 
def main():
    f=open('url.txt','a',encoding='utf-8')
    for page in range(1,500):
        time.sleep(8)
        print(page)
        args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E3%83%95%E3%82%A7%E3%82%B9%E3%83%91%E3%83%83%E3%82%AF&page='+str(page+1)+'&keywords=%E3%83%95%E3%82%A7%E3%82%B9%E3%83%91%E3%83%83%E3%82%AF&ie=UTF8&qid=1547370397'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E3%81%8A%E3%82%84%E3%81%A4&page='+str(page+1)+'&keywords=%E3%81%8A%E3%82%84%E3%81%A4&ie=UTF8&qid=1547189345'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E3%82%B3%E3%83%B3%E3%82%BF%E3%82%AF%E3%83%88%E3%83%AC%E3%83%B3%E3%82%BA%E3%83%BB%E3%82%AB%E3%83%A9%E3%82%B3%E3%83%B3&page='+str(page+1)+'&keywords=%E3%82%B3%E3%83%B3%E3%82%BF%E3%82%AF%E3%83%88%E3%83%AC%E3%83%B3%E3%82%BA%E3%83%BB%E3%82%AB%E3%83%A9%E3%82%B3%E3%83%B3&ie=UTF8&qid=1546938756'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E5%A4%A7%E5%9E%8B%E5%AE%B6%E9%9B%BB&page='+str(page+1)+'&keywords=%E5%A4%A7%E5%9E%8B%E5%AE%B6%E9%9B%BB&ie=UTF8&qid=1546937555'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E8%96%AC&page='+str(page+1)+'&keywords=%E8%96%AC&ie=UTF8&qid=1546926519'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E9%A3%9F%E5%93%81&page='+str(page+1)+'&keywords=%E9%A3%9F%E5%93%81&ie=UTF8&qid=1546925627'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3A%E7%94%9F%E6%B4%BB%E5%AE%B6%E9%9B%BB&page='+str(page+1)+'&keywords=%E7%94%9F%E6%B4%BB%E5%AE%B6%E9%9B%BB&ie=UTF8&qid=1546924746'
        # args='https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?rh=i%3Aaps%2Ck%3Aシャンプー&page='+str(page+1)+'&keywords=シャンプー&ie=UTF8&qid=1546909420'
        # args = 'https://www.amazon.co.jp/s/ref=sr_pg_'+str(page+1)+'?fst=as%3Aon&rh=n%3A52374051%2Cn%3A5267102051%2Cn%3A169667011%2Ck%3Aシャンプー&page='+str(page+1)+'&keywords=シャンプー&ie=UTF8'
        Get_Images(args,f)
    f.close()
    return None
 
 
if __name__ == '__main__':
    main()
