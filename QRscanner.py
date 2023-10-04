import pymysql
import cv2
import pyzbar.pyzbar as pyzbar
import requests
import json 

# QR Code and Barcode Scanner
used_codes = []
data_list = []

try:
    f = open("qrbarcode_data.txt", "r", encoding="utf8")
    data_list = f.readlines()
except FileNotFoundError:
    pass
else:
    f.close()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

headerInfo = {"Content-Type" : "application/json"}

for i in data_list:
    used_codes.append(i.rstrip('\n'))

while True:
    success, frame = cap.read()

    for code in pyzbar.decode(frame):
        cv2.imwrite('qrbarcode_image.png', frame)
        my_code = code.data.decode('utf-8')
        if my_code not in used_codes:
            print("인식 성공:", my_code)
            used_codes.append(my_code)

            # Send the code to the REST API
            api_url = "http://10.150.150.179:8080/api/camera"
            payload = {'code': my_code}
            jLoad = json.dumps(payload)
            response = requests.post(api_url, data=jLoad, headers=headerInfo)
            if response.status_code == 200:
                print("Code sent to API successfully!")
                print(response.json())
            else:
                print("Failed to send code to API.")
                print(response.json())

            f2 = open("qrbarcode_data.txt", "a", encoding="utf8")
            f2.write(my_code + '\n')
            f2.close()
        else:
            print("이미 인식된 코드입니다.!!!")

    cv2.imshow('QRcode Barcode Scan', frame)
    cv2.waitKey(1)