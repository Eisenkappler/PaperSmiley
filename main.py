import requests
import cv2
import numpy as np
import imutils

url = "http://192.168.0.109:8080/shot.jpg"

def convertImagetoBinary(img):
    img = cv2.GaussianBlur(img,(7,7),1)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    return img


def findrectangle(img,original):
    contours = []
    contours,hierachy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,  0.01*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) == 4 and area > 2000:
            #print(contours)
            print(approx)
            cv2.drawContours(original,cnt,-1,(255,30,165),5)
            for pt in approx:
                print(pt)
                cv2.circle(original,pt[0],10,(0,0,0),-1)

    return original

# While loop to con1tinuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.imread(r"C:\Users\nikol\OneDrive\Desktop\Samples\rectangle.png")
    null,imggray = convertImagetoBinary(img)

    imggray = imutils.resize(imggray, width=1920, height=1080)
    img = findrectangle(imggray,img)
    img = imutils.resize(img, width=1920, height=1080)
    #img = cv2.bitwise_not(img)
    cv2.imshow("Android_cam", img)
    cv2.imshow("test", imggray)

    #cv2.imwrite(r"C:\Users\nikol\OneDrive\Desktop\Samples\original.png",img)

# Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
