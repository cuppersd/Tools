# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json


http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = "yt-hM3Q_CTF_SsfwY2XTTxVAjswSDBxo"
secret = "prUQjugxRW1QJW_wVhue55dHkLKIrjBw"
filepath = r"3.jpg"
boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
fr = open(filepath, 'rb')
data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
data.append('Content-Type: %s\r\n' % 'application/octet-stream')
data.append(fr.read())
fr.close()
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
data.append('2')
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
data.append(
    "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
data.append('--%s--\r\n' % boundary)

for i, d in enumerate(data):
    if isinstance(d, str):
        data[i] = d.encode('utf-8')

http_body = b'\r\n'.join(data)

# build http request
req = urllib.request.Request(url=http_url, data=http_body)

# header
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)


from PIL import Image, ImageDraw, ImageFont
im = Image.open(filepath)
draw = ImageDraw.Draw(im)
point_size=1 # 点的大小

    




try:
    # post data to server
    resp = urllib.request.urlopen(req, timeout=5)
    # get response
    qrcont = resp.read()
    for g in range(0,2):
        ss=json.loads(qrcont.decode('utf-8'))['faces'][g]['landmark']
    # if you want to load as json, you should decode first,
    # for example: json.loads(qrount.decode('utf-8'))
        print(len(ss.keys()))
        for xxx in ss.keys():
            print(xxx)
            x,y=ss[xxx]['x'],ss[xxx]['y']
            draw.ellipse((x-point_size, y-point_size,x+point_size, y+point_size),fill = (0, 255, 0)) # fill是填充颜色

    
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))

im.show()