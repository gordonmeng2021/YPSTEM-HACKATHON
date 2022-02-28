from threading import *
import time
import cv2


face_cascade = cv2.CascadeClassifier('Flask/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

def focus():
    global isFocus
    isFocus = True
    
state = True
focusedTime = 0
notfocusedTime =0

class Hello(Thread):
    
      
   def run(self):
      global isFocus,focusedTime,notfocusedTime
      while state:
             
         startTimer=time.time()
         isFocus = False
    # Read the frame
         _, img = cap.read()
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         faces = face_cascade.detectMultiScale(gray, 1.1, 4)
         for (x, y, w, h) in faces:
            if len(faces)<2:
               focus()
               
            
               # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
               
        # change state if has face
               
               
         if isFocus == False:
            print("You are not focusing")
            endTimer=time.time()
            notfocusedTime += (endTimer-startTimer) 
         else:
            print("You are okay")
            endTimer=time.time()
            focusedTime += (endTimer-startTimer)
            
         
            
         k = cv2.waitKey(1) & 0xff
         if k==27:
                break
         
class Hi(Thread):
   def run(self):   
      global a,state
      for _ in range(3):
         # print("here??????")
         # changing state
         a =input()
         if a =="stop":
            state =False
            print("You have focused :", str(int(focusedTime)),'s')
            print("You have not focused :", str(int(notfocusedTime)),'s')     
            # print(state)
         if a =="start":
            state =True
            
            # print(state)
            t1.run()
            t2.run()
t1=Hello()
t2 =Hi()
# Think about how to stop again 
t1.start()
t2.start()