import socket
import cv2
import numpy as np
from _thread import *

trackerKCF = cv2.TrackerKCF_create()

#face_detector = cv2.CascadeClassifier('C:/Users/qhfn7/anaconda3/envs/Yolo_V4/Library/etc/haarcascades/haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier('C:/Users/qhfn7/anaconda3/envs/Yolo_V4/Library/etc/haarcascades/haarcascade_upperbody.xml')
        

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


#HOST = '172.30.1.63'
HOST = '192.168.0.8'
PORT = 8485

# TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))

print('Socket created')

# 서버의 아이피와 포트번호 지정
s.bind((HOST, PORT))
print('Socket bind complete')
# 클라이언트의 접속을 기다린다. (클라이언트 연결을 1개까지 받는다)
s.listen(10)
print('Socket now listening')

# 연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn, addr = s.accept()

while True:
    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')

    # data를 디코딩한다.
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        print('no body in cam')
        conn.sendall("no".encode())
        continue
    else:
        trackObjectTuple = (faces[0,0], faces[0,1], faces[0,2], faces[0,3])
        result = trackerKCF.init(frame, trackObjectTuple)
        print('start tracking the user')
        conn.sendall("start".encode())
        break


while True:
    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')

    # data를 디코딩한다.
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

    isUpdated, trackObjectTuple = trackerKCF.update(frame) 
    if isUpdated: 
        x1 = (int(trackObjectTuple[0]) , int(trackObjectTuple[1]) ) 
        x2 = (int(trackObjectTuple[0] + trackObjectTuple[2]), int(trackObjectTuple[1] + trackObjectTuple[3])) 
        cv2.rectangle(frame, x1, x2, (255, 0, 0), 2) 
    cv2.imshow("track object", frame) 

    x_frame = str(int(trackObjectTuple[0] + (trackObjectTuple[2]/2)))
    y_frame = str(int(trackObjectTuple[1] + (trackObjectTuple[3]/2)))

    frame_data = x_frame + y_frame
    print("\nx frame : ", str(x_frame),"\ty frame : ", str(y_frame), "\tframe : ", str(frame_data))
    #msg = frame_data
    #print("msg : ", frame_data, "\n")
    #conn.send(msg.encode())
    
    # 좌측 상단
    if int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 270 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 100:
        print('low left')
        msg = "w"
        conn.send(msg.encode())

    # 좌측 중간
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 270 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 100 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) <= 190:
        print('mid left')
        msg = "s"
        conn.send(msg.encode())
    
    # 좌측 하단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 270 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 480:
        print('high left')
        msg = "x"
        conn.send(msg.encode())

    # 중간 상단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) >= 270 and \
        int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 370 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 100:
        print('low front')
        msg = "e"
        conn.send(msg.encode())

    # 중간 중간
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) >= 270 and \
        int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 370 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 100 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) <= 190:
        print('mid front')
        msg = "d"
        conn.send(msg.encode())
    
    # 중간 하단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) >= 270 and \
        int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 370 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 480:
        print('high front')
        msg = "c"
        conn.send(msg.encode())
    
    # 우측 상단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 640 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 100:
        print('low right')
        msg = "r"
        conn.send(msg.encode())

    # 우측 중단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 640 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 100 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) <= 190:
        print('mid right')
        msg = "f"
        conn.send(msg.encode())

    # 우측 하단
    elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) < 640 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 480:
        print('high right')
        msg = "v"
        conn.send(msg.encode())

    if int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) <= 50 and \
        int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 0:
        print("User very close")
        msg = "q"
        conn.send(msg.encode())


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
s.close()