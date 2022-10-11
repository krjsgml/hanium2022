import cv2
import socket
import numpy as np
from _thread import *
from bluetooth import *

# socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

## bluetooth
bluetooth_socket = BluetoothSocket( RFCOMM )
bluetooth_socket.connect(('98:DA:60:05:D1:74',1))
print('bluetooth connect')

## TCP 사용
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
# s.connect(('172.30.1.63', 8485))
tcp_socket.connect(('192.168.0.8', 8485))

## webcam 이미지 capture
cam = cv2.VideoCapture(0)
 
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 640);
cam.set(4, 480);
 
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]


print ('>> Connect Server')

flag = []
send_flag = 1
recv_flag = 0
tracking_flag = 0

bluetooth_socket.send("2")

while True:
    if send_flag == 1:
        # 비디오의 한 프레임씩 읽는다.
        # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
        ret, frame = cam.read()
        # cv2. imencode(ext, img [, params])
        # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        # frame을 String 형태로 변환
        data = np.array(frame)
        stringData = data.tobytes()
 
        #서버에 데이터 전송
        #(str(len(stringData))).encode().ljust(16)
        tcp_socket.sendall((str(len(stringData))).encode().ljust(16) + stringData)
        
        recv_flag = 1
        
        if tracking_flag == 1:
            send_flag = 0
            
    if recv_flag == 1:
        tcp_socket_data = tcp_socket.recv(1024)
        if tcp_socket_data.decode() == 'start':
            tracking_flag = 1
        
        data_bluetooth = tcp_socket_data.decode()
        bluetooth_socket.send(data_bluetooth)
        print('send to bluetooth : ')
        print(data_bluetooth)
        
        if tcp_socket_data == "q":
            bluetooth_socket.send("1")
            print('stop')
            break
        
        send_flag = 1
        recv_flag = 0

        
cam.release()
tcp_socket.close()
bluetooth_socket.close()
