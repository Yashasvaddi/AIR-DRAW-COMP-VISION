import cv2 as cv2
import numpy as np
import mediapipe as mp
import math as m
from collections import deque
import google.generativeai as genai
import camera_selector as cs
import threading as th
import pyttsx3
import speech_recognition as sr
import sys
import PIL.Image


genai.configure(api_key="AIzaSyC3vNkSnEJl-eFloSm9M4Bw0F_cJv2vusY")
model = genai.GenerativeModel("gemini-2.0-flash")

num=0
speech=""
thread_flag=False
answer=""
answer1=""

def image_prcoess():
    global answer1
    print("Image being sent to gemini")
    image_path="C:\\Users\\YASHAS\\Pictures\\virtual ss\\drawing.png"
    image=PIL.Image.open(image_path)
    response=model.generate_content([image,"What is the result of the expression on the screen?"])
    answer1=response.text
    print(answer1)

def wrap_text(text, max_width, font, font_scale, thickness):
    """Splits text into multiple lines to fit inside OpenCV window."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_size, _ = cv2.getTextSize(test_line, font, font_scale, thickness)

        if text_size[0] > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    lines.append(current_line)  # Add the last line
    return lines

def assistant():
    global answer, flag,thread_flag
    recognizer=sr.Recognizer()
    engine=pyttsx3.init()
    engine.say("Hello")
    while not thread_flag:
        if engine.stop():
            engine=pyttsx3.init()
        with sr.Microphone() as source:
            print("Listening....")
            audio=recognizer.listen(source)
            try:
                question=recognizer.recognize_google(audio)
                print(question)
                if(question=="exit"):
                    engine.say("Exiting")
                    flag=False
                    break
                response=model.generate_content(question)
                response_text=response.text
                answer=response_text
                if not engine._inLoop:
                    engine.say(response_text)
                    engine.runAndWait()
            except sr.UnknownValueError:
                print("Unable to understand")
    else:
        print("Assistant thread Closed")
        engine.stop()

def live_caption():
    global flag,speech,thread_flag
    recognizer=sr.Recognizer()
    engine=pyttsx3.init()
    while not thread_flag:
        with sr.Microphone() as source:
            print("Listening....")
            audio=recognizer.listen(source)
            try:
                question=recognizer.recognize_google(audio)
                if(question=="exit"):
                    engine.say("Exiting")
                    flag=False
                    break
                speech+=question+" "
                print(speech)
            except sr.UnknownValueError:
                print("Unable to understand")
    else:
        print("Caption thread Closed")
        engine.stop()


def save_canvas(image):
    filename = r"C:\Users\YASHAS\Pictures\virtual ss\drawing.png"
    cv2.imwrite(filename, image)
    print(f"Canvas saved as {filename}")

camflag=True
i=cs.camera_selector()
if i!=0:
    camflag=False
cap=cv2.VideoCapture(i)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands()
mp_draw=mp.solutions.drawing_utils  
flag =True
if not cap.isOpened():
    print("camera error!!")
else:
    while(True):
        ret,frame=cap.read()
        if (camflag):
            frame=cv2.flip(frame,1)
        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        backdrop_source="C:\\New folder\\codes\\college stuff\\AIR-DRAW-COMP-VISION\\miniproject sem 4\\Backdrop.webp"
        window=cv2.imread(backdrop_source)
        result=hands.process(rgb_frame)
        rect1x1,rect1y1=int(10),int(20)
        rect1x2,rect1y2=int(120),int(65)

        if result.multi_hand_landmarks:
            cv2.rectangle(window,(rect1x1,rect1y1),(rect1x2,rect1y2),(255,255,255),2)
            cv2.putText(window,"Air Draw",(25,45),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.rectangle(window,(rect1x1+160,rect1y1),(rect1x2+160,rect1y2),(255,255,255),2)
            cv2.putText(window,"Slide Show",(175,45),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
            cv2.rectangle(window,(rect1x1+310,rect1y1),(rect1x2+310,rect1y2),(255,255,255),2)
            cv2.putText(window,"Caption",(335,45),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.rectangle(window,(rect1x1+460,rect1y1),(rect1x2+460,rect1y2),(255,255,255),2)
            cv2.putText(window,"Assistant",(480,45),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,255,255),1,cv2.LINE_AA)
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(window,hand_landmarks,mp_hands.HAND_CONNECTIONS) 
                h,w,_=window.shape
                thumb=hand_landmarks.landmark[4]
                index=hand_landmarks.landmark[8]
                x1,y1=int(thumb.x*w),int(thumb.y*h)
                x2,y2=int(index.x*w),int(index.y*h)
                cv2.rectangle(window,(x1,y1),(x2,y2),(0,0,0),2)
                distance=int((m.sqrt((x2-x1)**2+(y2-y1)**2)))
                if ((rect1x1<int((x1+x2)/2)<rect1x2 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50)):
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)
                    cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                    window[:]=255
                    bpoints = [deque(maxlen=1024)]
                    gpoints = [deque(maxlen=1024)]
                    rpoints = [deque(maxlen=1024)]
                    ypoints = [deque(maxlen=1024)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
                    colorIndex = 0
                    while(True):
                        window=np.zeros((471, 636, 3)) + 255
                        ret,frame=cap.read()
                        if (camflag):
                            frame=cv2.flip(frame,1)
                        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                        result=hands.process(rgb_frame)
                        rect1x1,rect1y1=int(10),int(410)
                        rect1x2,rect1y2=int(120),int(440)
                        #AIR CANVAS#

                        if result.multi_hand_landmarks:
                            cv2.rectangle(window,(rect1x1,rect1y1),(rect1x2,rect1y2),(0,0,0),2)
                            cv2.putText(window,"QUIT",(35,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                            cv2.rectangle(window,(rect1x1+480,rect1y1),(rect1x2+510,rect1y2),(0,0,0),2)
                            cv2.putText(window,"SAVE",(525,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                            for hand_landmarks in result.multi_hand_landmarks:
                                # mp_draw.draw_landmarks(window,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                h,w,_=frame.shape
                                thumb=hand_landmarks.landmark[4]
                                index=hand_landmarks.landmark[8]
                                x1,y1=int(thumb.x*w),int(thumb.y*h)
                                x2,y2=int(index.x*w),int(index.y*h)
                                cv2.rectangle(window,(x1,y1),(x2,y2),(0,0,0),2)
                                distance=int((m.sqrt((x2-x1)**2+(y2-y1)**2)))
                                cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5) 
                                cv2.rectangle(window, (40, 1), (140, 65), (0, 0, 0), 2)
                                cv2.rectangle(window, (160, 1), (255, 65), (255, 0, 0), 2)
                                cv2.rectangle(window, (275, 1), (370, 65), (0, 255, 0), 2)
                                cv2.rectangle(window, (390, 1), (485, 65), (0, 0, 255), 2)
                                cv2.rectangle(window, (505, 1), (600, 65), (0, 255, 255), 2)
                                cv2.putText(window, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                                cv2.putText(window, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                                cv2.putText(window, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                                cv2.putText(window, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                                cv2.putText(window, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                                if result.multi_hand_landmarks:
                                    landmarks = []
                                    for handslms in result.multi_hand_landmarks:
                                        for lm in handslms.landmark:
                                            lmx = int(lm.x * 640)
                                            lmy = int(lm.y * 480)
                                            landmarks.append([lmx, lmy])
                                        mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)
                                        mp_draw.draw_landmarks(window, handslms, mp_hands.HAND_CONNECTIONS)

                                    fore_finger = (landmarks[8][0], landmarks[8][1])
                                    center1 = fore_finger
                                    thumb = (landmarks[4][0], landmarks[4][1])
                                    center=(int((center1[0]+thumb[0])/2),int((center1[1]+thumb[1])/2))
                                    distance=int(m.sqrt((center1[0]-thumb[0])**2+(center1[1]-thumb[1])**2))
                                    if(distance>110):
                                        cv2.line(frame,thumb,center1,(0,0,255),3)
                                        cv2.circle(frame, center, 3, (0, 255, 0), -1)
                                        cv2.line(window,thumb,center1,(0,0,255),3)
                                        cv2.circle(window, center, 5, (0,0,255), -1)
                                    else:
                                        cv2.line(frame,thumb,center1,(0,255,0),3)
                                        cv2.circle(frame, center, 3, (255, 0, 255), -1)
                                        cv2.line(window,thumb,center1,(0,255,0),3)
                                        cv2.circle(window, center, 5, (255, 0, 255), -1)

                                    if (thumb[1] - center[1] < 30):
                                        bpoints.append(deque(maxlen=512))
                                        blue_index += 1
                                        gpoints.append(deque(maxlen=512))
                                        green_index += 1
                                        rpoints.append(deque(maxlen=512))
                                        red_index += 1
                                        ypoints.append(deque(maxlen=512))
                                        yellow_index += 1

                                    elif center[1] <= 65:
                                        if 40 <= center[0] <= 140:
                                            bpoints = [deque(maxlen=512)]
                                            gpoints = [deque(maxlen=512)]
                                            rpoints = [deque(maxlen=512)]
                                            ypoints = [deque(maxlen=512)]
                                            blue_index = 0
                                            green_index = 0
                                            red_index = 0
                                            yellow_index = 0
                                            window[67:, :, :] = 255
                                        elif 160 <= center[0] <= 255:
                                            colorIndex = 0
                                        elif 275 <= center[0] <= 370:
                                            colorIndex = 1
                                        elif 390 <= center[0] <= 485:
                                            colorIndex = 2
                                        elif 505 <= center[0] <= 600:
                                            colorIndex = 3
                                    else:
                                        if colorIndex == 0:
                                            bpoints[blue_index].appendleft(center)
                                        elif colorIndex == 1:
                                            gpoints[green_index].appendleft(center)
                                        elif colorIndex == 2:
                                            rpoints[red_index].appendleft(center)
                                        elif colorIndex == 3:
                                            ypoints[yellow_index].appendleft(center)

                                points = [bpoints, gpoints, rpoints, ypoints]
                        for i in range(len(points)):
                            for j in range(len(points[i])):
                                if not points[i][j]:
                                    continue
                                for k in range(1, len(points[i][j])):
                                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                                        continue
                                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                                    cv2.line(window, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                        if (((rect1x1+480<int((x1+x2)/2)<rect1x2+510 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))):
                                    if(flag):
                                        cv2.putText(window,"IMAGE SAVED",(255,435),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,0),1,cv2.LINE_AA)
                                        save_canvas(window)  
                                        image_prcoess()
                                        flag=False
                        else:
                            flag=True
                        wrapped_lines = wrap_text(answer1, max_width=600, font=cv2.FONT_HERSHEY_COMPLEX, font_scale=0.7, thickness=1)
                        y = 350 
                        for line in wrapped_lines:
                            cv2.putText(window, line, (10, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
                            y += 25
                        cv2.imshow("Window",window)
                        cv2.imshow("frame",frame)  
                        thumb=hand_landmarks.landmark[4]
                        index=hand_landmarks.landmark[8]
                        x1,y1=int(thumb.x*w),int(thumb.y*h)
                        x2,y2=int(index.x*w),int(index.y*h) 
                        if ((cv2.waitKey(1) and (rect1x1<int((x1+x2)/2)<rect1x2 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))):
                            break    
                else:
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(255,255,255),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(0,0,0),5)
                    cv2.line(window,(x1,y1),(x2,y2),(255,0,0),3)
                    

                #SECOND BOX#

                if ((rect1x1+160<int((x1+x2)/2)<rect1x2+160 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50)):
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)
                    cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                    h, w, _ = frame.shape
                    window=cv2.resize(window, (w, h))
                    window[:]=255
                    bpoints = [deque(maxlen=1024)]
                    gpoints = [deque(maxlen=1024)]
                    rpoints = [deque(maxlen=1024)]
                    ypoints = [deque(maxlen=1024)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
                    colorIndex = 0
                    flag=True
                    click_flag=True
                    wallpaper_holder=False
                    while(True):
                        if wallpaper_holder:
                            window=cv2.imread(address)
                            window=cv2.resize(window, (w, h))
                        else:
                            window=np.zeros((471, 636, 3)) + 255
                        ret,frame=cap.read()
                        if (camflag):
                            frame=cv2.flip(frame,1)
                        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                        result=hands.process(rgb_frame)
                        rect1x1,rect1y1=int(10),int(410)
                        rect1x2,rect1y2=int(120),int(440)

                        if (((rect1x1+480<int((x1+x2)/2)<rect1x2+510 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))):
                            if(flag):
                              cv2.putText(window,"IMAGE SAVED",(255,435),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,0),1,cv2.LINE_AA)
                              save_canvas(window)  
                              flag=False
                        else:
                            flag=True

                        if result.multi_hand_landmarks:
                            for hand_landmarks in result.multi_hand_landmarks:
                                mp_draw.draw_landmarks(window,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                h,w,_=frame.shape
                                thumb=hand_landmarks.landmark[4]
                                index=hand_landmarks.landmark[8]
                                x1,y1=int(thumb.x*w),int(thumb.y*h)
                                x2,y2=int(index.x*w),int(index.y*h)
                                cv2.rectangle(window,(rect1x1,rect1y1),(rect1x2,rect1y2),(0,0,0),2)
                                cv2.putText(window,"QUIT",(35,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                                cv2.rectangle(window,(rect1x1+480,rect1y1),(rect1x2+510,rect1y2),(0,0,0),2)
                                cv2.putText(window,"SAVE",(525,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                                cv2.rectangle(window,(x1,y1),(x2,y2),(0,0,0),2)
                                cv2.rectangle(window,(rect1x1+20,rect1y1-170),(rect1x2-20,rect1y2-170),(0,0,0),-1)
                                cv2.putText(window,"<",(int((rect1x1+rect1x2)/2)-5,int((rect1y1-170+rect1y2-160)/2)),cv2.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
                                cv2.rectangle(window,(rect1x1+530,rect1y1-170),(rect1x2+510-20,rect1y2-170),(0,0,0),-1)
                                cv2.putText(window,">",(int((rect1x1+480+rect1x2+510)/2)+5,int((rect1y1-170+rect1y2-170)/2)+7),cv2.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
                                distance=int((m.sqrt((x2-x1)**2+(y2-y1)**2)))
                                cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)  
 
                        thumb=hand_landmarks.landmark[4]
                        index=hand_landmarks.landmark[8]
                        x1,y1=int(thumb.x*w),int(thumb.y*h)
                        x2,y2=int(index.x*w),int(index.y*h) 
                        if ((cv2.waitKey(1) and (rect1x1+530<int((x1+x2)/2)<rect1x2+510-20 and rect1y1-170<int((y1+y2)/2)<rect1y2-170)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))and click_flag):
                            num+=1
                            if num>12:
                                num=1
                            address=fr'C:\Users\YASHAS\Pictures\ppt\img{num}.jpg'
                            window=cv2.imread(address)    
                            click_flag=False  
                            wallpaper_holder=True 
                        if ((cv2.waitKey(1) and (rect1x1+20<int((x1+x2)/2)<rect1x2-20 and rect1y1-170<int((y1+y2)/2)<rect1y2-170)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))and click_flag):
                            num-=1
                            if num<=0:
                                num=12
                            address=fr'C:\Users\YASHAS\Pictures\ppt\img{num}.jpg'
                            window=cv2.imread(address)    
                            click_flag=False  
                            wallpaper_holder=True
                        window=cv2.resize(window, (w, h))
                        cv2.imshow("Window",window)
                        cv2.imshow("frame",frame) 
                        if ((cv2.waitKey(1) and (rect1x1<int((x1+x2)/2)<rect1x2 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))):
                            break
                           
                else:
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(255,255,255),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(0,0,0),5)
                    cv2.line(window,(x1,y1),(x2,y2),(255,0,0),3)


                #THIRD BOX#
                if ((rect1x1+310<int((x1+x2)/2)<rect1x2+310 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50)):
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)
                    cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                    window[:]=255
                    bpoints = [deque(maxlen=1024)]
                    gpoints = [deque(maxlen=1024)]
                    rpoints = [deque(maxlen=1024)]
                    ypoints = [deque(maxlen=1024)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
                    colorIndex = 0
                    flag=True
                    thread_flag=False
                    # if not t3.is_alive():
                    print("Caption thread started")
                    t3=th.Thread(target=live_caption)
                    t3.start()
                    while(True):
                        window=np.zeros((471, 636, 3)) + 255
                        cv2.putText(window,"WELCOME TO LIVE CAPTIONING",(15,30),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),2,cv2.LINE_AA)
                        ret,frame=cap.read()
                        if (camflag):
                            frame=cv2.flip(frame,1)
                        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                        result=hands.process(rgb_frame)
                        if (speech):
                            wrapped_lines = wrap_text(speech, max_width=600, font=cv2.FONT_HERSHEY_COMPLEX, font_scale=0.7, thickness=1)
                            y = 90 
                            for line in wrapped_lines:
                                cv2.putText(window, line, (10, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
                                y += 25  
                        rect1x1,rect1y1=int(10),int(410)
                        rect1x2,rect1y2=int(120),int(440)
                        cv2.rectangle(window,(rect1x1,rect1y1),(rect1x2,rect1y2),(0,0,0),2)
                        cv2.putText(window,"QUIT",(35,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                        cv2.rectangle(window,(rect1x1+480,rect1y1),(rect1x2+510,rect1y2),(0,0,0),2)
                        cv2.putText(window,"SAVE",(525,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)

                        if (((rect1x1+480<int((x1+x2)/2)<rect1x2+510 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))):
                            if(flag):
                              cv2.putText(window,"IMAGE SAVED",(255,435),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,0),1,cv2.LINE_AA)
                              save_canvas(window)  
                              flag=False
                              thread_flag=True
                        else:
                            flag=True

                        if result.multi_hand_landmarks:
                            for hand_landmarks in result.multi_hand_landmarks:
                                mp_draw.draw_landmarks(window,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                h,w,_=frame.shape
                                thumb=hand_landmarks.landmark[4]
                                index=hand_landmarks.landmark[8]
                                x1,y1=int(thumb.x*w),int(thumb.y*h)
                                x2,y2=int(index.x*w),int(index.y*h)
                                cv2.rectangle(window,(x1,y1),(x2,y2),(0,0,0),2)
                                distance=int((m.sqrt((x2-x1)**2+(y2-y1)**2)))
                                cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)  

                        cv2.imshow("Window",window)
                        cv2.imshow("frame",frame)  
                        thumb=hand_landmarks.landmark[4]
                        index=hand_landmarks.landmark[8]
                        x1,y1=int(thumb.x*w),int(thumb.y*h)
                        x2,y2=int(index.x*w),int(index.y*h) 
                        if ((cv2.waitKey(1) and (rect1x1<int((x1+x2)/2)<rect1x2 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))):
                            thread_flag=True
                            t3.join()
                            break                     
                else:
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(255,255,255),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(0,0,0),5)
                    cv2.line(window,(x1,y1),(x2,y2),(255,0,0),3)


                #LAST BOX#
                if ((rect1x1+460<int((x1+x2)/2)<rect1x2+460 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50)):
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                    cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)
                    cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                    window = np.full((471, 636, 3), (169, 169, 169), dtype=np.uint8)
                    bpoints = [deque(maxlen=1024)]
                    gpoints = [deque(maxlen=1024)]
                    rpoints = [deque(maxlen=1024)]
                    ypoints = [deque(maxlen=1024)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
                    colorIndex = 0
                    flag=True
                    thread_flag=False
                    # if not t1.is_alive():
                    print("Assistant thread started")
                    t1=th.Thread(target=assistant,daemon=True)
                    t1.start()
                    while(True):
                        window=np.zeros((471, 636, 3)) + 255
                        cv2.putText(window,"WELCOME TO YOUR PERSONAL CHATBOT",(5,25),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                        ret,frame=cap.read()
                        if (camflag):
                            frame=cv2.flip(frame,1)
                        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                        result=hands.process(rgb_frame)
                        rect1x1,rect1y1=int(10),int(410)
                        rect1x2,rect1y2=int(120),int(440)
                        cv2.rectangle(window,(rect1x1,rect1y1),(rect1x2,rect1y2),(0,0,0),2)
                        cv2.putText(window,"QUIT",(35,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                        cv2.rectangle(window,(rect1x1+480,rect1y1),(rect1x2+510,rect1y2),(0,0,0),2)
                        cv2.putText(window,"SAVE",(525,435),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1,cv2.LINE_AA)
                        wrapped_lines = wrap_text(answer, max_width=600, font=cv2.FONT_HERSHEY_COMPLEX, font_scale=0.7, thickness=1)
                        y = 60 
                        for line in wrapped_lines:
                            cv2.putText(window, line, (10, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
                            y += 25
                        if (((rect1x1+480<int((x1+x2)/2)<rect1x2+510 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))):
                            if(flag):
                              cv2.putText(window,"IMAGE SAVED",(255,435),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,0),1,cv2.LINE_AA)
                              save_canvas(window)  
                              flag=False
                        else:
                            flag=True

                        if result.multi_hand_landmarks:
                            for hand_landmarks in result.multi_hand_landmarks:
                                mp_draw.draw_landmarks(window,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                h,w,_=frame.shape
                                thumb=hand_landmarks.landmark[4]
                                index=hand_landmarks.landmark[8]
                                x1,y1=int(thumb.x*w),int(thumb.y*h)
                                x2,y2=int(index.x*w),int(index.y*h)
                                cv2.rectangle(window,(x1,y1),(x2,y2),(0,0,0),2)
                                distance=int((m.sqrt((x2-x1)**2+(y2-y1)**2)))    
                                cv2.line(window,(x1,y1),(x2,y2),(0,0,255),3)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),7,(0,0,0),5)
                                cv2.circle(window,(int((x1+x2)/2),int((y1+y2)/2)),9,(100,100,100),5)  

                        cv2.imshow("Window",window)
                        cv2.imshow("frame",frame)  
                        thumb=hand_landmarks.landmark[4]
                        index=hand_landmarks.landmark[8]
                        x1,y1=int(thumb.x*w),int(thumb.y*h)
                        x2,y2=int(index.x*w),int(index.y*h) 
                        if ((cv2.waitKey(1) and (rect1x1<int((x1+x2)/2)<rect1x2 and rect1y1<int((y1+y2)/2)<rect1y2)and(int(distance)<=50))or(cv2.waitKey(1)==ord('x'))):
                            thread_flag=True
                            t1.join()
                            break           

        cv2.namedWindow("Window",cv2.WINDOW_NORMAL)
        cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
        cv2.imshow("frame",frame)
        cv2.imshow("Window",window)
        if cv2.waitKey(1) == ord('x'):
            thread_flag=True
            cap.release()  # Release the camera
            cv2.destroyAllWindows()
            sys.exit()
            break
        