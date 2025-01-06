from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import simpledialog
from tkinter import filedialog

import os
import cv2


main = tkinter.Tk()
main.title("A Forest Fire Identification Method for Unmanned Aerial Vehicle Monitoring Video Images") #designing main screen
main.geometry("1300x1200")

global filename

def ColorFeaturesDetectFire(frame):
    msg = "No Fire Detected"
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    print(no_red)
    if int(no_red) > 4000:
        msg = "Fire detected"
    return msg, mask

def upload():
    global filename
    filename = filedialog.askopenfilename(initialdir="UAV_Videos")
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");
    
def detectFire():
    global filename
    video = cv2.VideoCapture(filename)
    previous_frame = None
    while(True):
        ret, frame = video.read()
        if ret == True:
            msg, temp = ColorFeaturesDetectFire(frame)
            img_rgb = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
            prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)
            if (previous_frame is None):
                previous_frame = prepared_frame
                continue
            if (previous_frame is None):
                previous_frame = prepared_frame
                continue
            diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
            previous_frame = prepared_frame
            kernel = np.ones((5, 5))
            diff_frame = cv2.dilate(diff_frame, kernel, 1)
            thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            '''
            for contour in contours:
                if cv2.contourArea(contour) < 50:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(img=img_rgb, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
            '''    
            cv2.putText(frame, msg, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.imshow('Fire Detector', frame)
            cv2.imshow("Motion Image",temp)
            if cv2.waitKey(600) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
    
    

font = ('times', 16, 'bold')
title = Label(main, text='A Forest Fire Identification Method for Unmanned Aerial Vehicle Monitoring Video Images')
title.config(bg='LightGoldenrod1', fg='medium orchid')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=25,width=140)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)


font1 = ('times', 12, 'bold')
uploadButton = Button(main, text="Upload UAV Forest Fire Video", command=upload)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

preButton = Button(main, text="Run Motion Detection, Colour Features and Wavlet Transfrom to Detect File", command=detectFire)
preButton.place(x=350,y=100)
preButton.config(font=font1) 


main.config(bg='OliveDrab2')
main.mainloop()
