import re
import requests
import sys
import uuid
import urllib.request
import random
import traceback
import time
import os

 
pattern = r'"hiRes":"https://images-na.ssl-images-amazon.com/images/I/([\w\d\s:/.-]+?)jpg'
regex = re.compile(pattern)
 
 
def Get_Images(URL):
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
    """
    A function that returns all image URLs found within a given website
    """
 
    print("\nAttempting to download images from the given URL.\n")
    r = requests.get(URL,headers=headers)
 
    if r.status_code != 200:
        print("Error retrieving the desired website. Aborting! Try again later.\n\n")
        sys.exit(1)
    elif r.status_code == 200:
        html = r.text
        All_Images = re.findall(regex, html)
 
        # You can either print the URLs found or return it as a list:
        print("\nPrinting all images found in the webpage:\n")
        for image in All_Images:
            img_url = 'https://images-na.ssl-images-amazon.com/images/I/'+image+'jpg'
            print(img_url)
            if os.path.exists('../img/'+image+'jpg'):
                print("下载过了！")
                continue
            urllib.request.urlretrieve(img_url,'../img/'+image+'jpg')
            print("已下载")
            time.sleep(3)
 
    return None
 
 
def main():
    f=open('url.txt','r',encoding='utf-8').readlines()
    ff=open('download.txt','a',encoding='utf-8')
    for args in f:
        ff.write(args)
        # time.sleep(3)
        try:
            Get_Images(args.strip())
        except:
            print(traceback.print_exc())

            print("出现异常")
            continue
    ff.close()
    return None
 
 
if __name__ == '__main__':
    main()