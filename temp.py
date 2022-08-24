import time
import numpy as np
import cv2

time.sleep(3) #helps to sleep for 3sec which helpus to making our setup ready
count = 0
background = 0
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

for i in range(30):  
    ret, background = cap.read()

background = np.flip(background,axis=1)    
    

while(cap.isOpened()):
    ret, frame = cap.read() # it returns boolean value
    
    #if frame is properly read then ret will be true
    if not ret:
        print("Frame can't be read correctly")
        break
    count += 1
    frame = np.flip(frame,axis=1)
    hsv_img  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #lower mask
    lower_red1 = np.array([0,120,70])
    higher_red1 = np.array([10,255,255])
    
    mask1 = cv2.inRange(hsv_img,lower_red1,higher_red1)
    
    #higher mask
    lower_red2 = np.array([170,120,70])
    higher_red2 = np.array([180,255,255])
    
    mask2 = cv2.inRange(hsv_img,lower_red2,higher_red2)
    
    mask = mask1+mask2
    
    # we use morphological operation open and dilate
    # morph-open it uses erosion followed by dilation to remove noise
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    
    frame[np.where(mask == 255)] = background[np.where(mask == 255)]
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
out.release()
cap.release()
cv2.destroyAllWindows()
    
    