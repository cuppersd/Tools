# 对人脸区域矩阵转化成jpg文件流的形式
import requests
img_encode = cv2.imencode('.jpg', frame)[1]  # frame为视频文件中读取的一帧
data_encode = np.array(img_encode)
str_encode = data_encode.tostring()
r = requests.post(' http://192.168.1.162:7000/facebox/', files={'content':str_encode})  # str_encode相当于open(file, "rb")
