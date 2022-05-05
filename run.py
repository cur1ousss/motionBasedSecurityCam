# videos will be recorded in the same folder as the code
from logging import captureWarnings
import cv2
import time
import datetime

captured=cv2.VideoCapture(0)


# using harcascade classifier to detect faces, pretrained and prebuilt by OpenCV
                                        # base dir + specific
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
body_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_fullbody.xml")

# classifier accepts only grayscale image so convert


detection=False

detection_stopped_time=None
timer_started=False

seconds_to_record_afterDetection=5

# frameSize of video to be recorded
frameSize=(int(captured.get(3)),int(captured.get(4)))   # 3 4 indices of width, height 

# setup 4 character code for video format that'll be saved {mp4 format}
fourcc=cv2.VideoWriter_fourcc(*"mp4v")

while True:
    temp, frame=captured.read()

    grayedImage=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces=face_cascade.detectMultiScale(grayedImage,1.4,5)
                                                    # scale factor # neighbours 
                                                    # affects speed accuracy
    
    bodies=body_cascade.detectMultiScale(grayedImage,1.4,5)


    for(x,y,width,height) in faces:
        cv2.rectangle(frame, (x,y), (x+width,y+height),(255,0,0),3)

    if len(faces)+len(bodies)>0:
        if detection:   
            timer_started=False
        else:
            detection=True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            #output stream
            out=cv2.VideoWriter(f"{current_time}.mp4",fourcc,20,frameSize)
                                    # frameRate
            print("Started Recording !!!")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >=seconds_to_record_afterDetection:
                detection=False
                timer_started=False
                out.release()
                print("Stopped Recording !!!zzz")
        else:
            timer_started=True
            detection_stopped_time=time.time()


    if detection:
        out.write(frame)

    cv2.imshow("Captured Window",frame)

    if cv2.waitKey(1)==ord('q'):
        break

out.release()
captured.release()
cv2.destroyAllWindows()