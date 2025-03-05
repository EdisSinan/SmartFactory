import signal
import sys
import cv2
import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED
from gpiozero import LEDCharDisplay
GPIO.setmode(GPIO.BCM)
car_detection_pin=18
sensor_pin=23
pwmMotor1=PWMLED(24)
pwmMotor2=PWMLED(25)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(car_detection_pin, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
sensor_detected = False
sensor2_detected = False
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO_TRIGGER = 26
GPIO_ECHO = 19
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
display = LEDCharDisplay(13, 6, 5, 11,9,10,21, active_high=True)
i=0
ukutiji= False;
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

def sensor_callback(channel):
    global sensor_detected
    sensor_detected = not GPIO.input(sensor_pin)
    if not GPIO.input(sensor_pin):
       print("Item Detected")

       
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=sensor_callback, bouncetime=300)
thres = 0.45 # Threshold to detect object+

classNames = []
classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")
configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects: 
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

                    
    
    return img,objectInfo
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
   while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.55,0.2, objects=['bottle','cup'])
        dist = distance()
        if GPIO.input(car_detection_pin):
            print('Car is absent nothing to do')
            GPIO.output(17, 0)
            GPIO.output(22, 0)
            GPIO.output(27, 0)
        else:
            if(objectInfo==[]):
                if (not sensor_detected):
                    print('Prva traka se krece')
                    GPIO.output(17, 1)
                    pwmMotor1.value=0.4
                    GPIO.output(22, 0)
                    GPIO.output(27, 0)
                    GPIO.output(12, 1)
                    GPIO.output(16, 0)
                    sensor_detected=True                   
                else:
                    GPIO.output(12, 1)
                    while not ukutiji:
                     print('Kamera nije detektovala adekvatan predmet za reciklazu traka dva ide lijevo')
                     GPIO.output(22, 0)
                     GPIO.output(17, 0)
                     GPIO.output(27, 1)
                     pwmMotor2.value=0.7
                     sensor_detected=False
                     GPIO.output(12, 1)
                     GPIO.output(16, 0)
                     dist = distance()
                     print(dist)
                     if dist <7 and dist>0:
                       print("U kutiji")
                       if i<9:
                         i=i+1
                         charval= chr(ord('0') + i)
                         display.value = charval
                         print(i)
                         ukutiji=True 
                         break
                       else:
                         if(i == 9):
                           char= chr(ord('0') + i)
                           display.value = charval
                           print(i)
                           i=0
                           ukutiji=True
                           break
                         else:
                           print(i)
                           i=0
                           charval= chr(ord('0') + i)
                           display.value = charval
                           ukutiji = True 
                           break
                    else:
                       #ostaje isti broj
                       print("Nije nista palo")
            else: 
                if (not sensor_detected):
                    GPIO.output(17, 1)
                    GPIO.output(27, 0)
                    GPIO.output(22, 0)                    
                    pwmMotor1.value=0.45
                    sensor_detected=True
                else:
                    if (objectInfo[0][1]=='bottle'):
                        print('Detektovan predmet za reciklazu traka dva ide u desno')
                        GPIO.output(22, 1)
                        pwmMotor2.value=0.85
                        GPIO.output(17, 0)
                        GPIO.output(27, 0)
                        GPIO.output(12, 0)
                        GPIO.output(16, 1)
                        sensor_detected=False
                        time.sleep(2)
                    else:
                       while not ukutiji :
                        print('Detektovao sam nešto al nije za reciklažu, traka dva ide u lijevo')
                        GPIO.output(22, 0)
                        GPIO.output(17, 0)
                        GPIO.output(27, 1)
                        GPIO.output(12, 1)
                        GPIO.output(16, 0)
                        pwmMotor2.value=0.6
                        sensor_detected=False
                        GPIO.output(12, 1)
                        GPIO.output(16, 0)
                        dist = distance()
                        if dist< 7 and dist>0:
                         print("U kutiji")
                         if i<9:
                          i=i+1
                          charval= chr(ord('0') + i)
                          display.value = charval
                          print(i)
                          ukutiji = True
                          break
                         else:
                          if(i == 9):
                            char= chr(ord('0') + i)
                            display.value = charval
                            print(i)
                            ukutiji = True
                            i=0
                            break
                          else:
                            print(i)
                            i=0
                            ukutiji = True
                            break
                        sensor_detected=False
        cv2.imshow("Output",img)
        cv2.waitKey(1)
        sensor_detected = False
        ukutiji=False
