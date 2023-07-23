import csv
import cv2 as cv
import cvzone as cvz
from cvzone.HandTrackingModule import HandDetector
import time
import datetime

# Declaring the cap variable to start Camera activity
cap = cv.VideoCapture(0)
#To declare the size of the Window
cap.set(3,1920)
cap.set(4,1080)

detector = HandDetector(detectionCon=0.8)

# Class to access the elements from CSV file
class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None
        
#To check if answer is clicked from the boxes
    def update(self,cursor,bboxs):
        for x, box in enumerate(bboxs):
            x1,y1,x2,y2 = box
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns = x+1
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),cv.FILLED)



#importing CSV file
getFile = "Que.csv"
with open(getFile,newline='\n') as file:
    reader = csv.reader(file)
    datafile = list(reader)[1:]

#Creating Object for class MCQ
mcqList = []
for q in datafile:
    mcqList.append(MCQ(q))

t = len(mcqList)
quesNumber = 0
qTotal = len(datafile)

while True:
    ret, frame = cap.read()

    # To Flip the camera view to the original side
    hands, frame = detector.findHands(frame,flipType=True)
    dt = str(datetime.datetime.now())
    frame = cv.putText(frame,dt,(750,50),cv.FONT_HERSHEY_PLAIN,2,(255,255,255),4)
    if quesNumber < qTotal:

        mcq = mcqList[quesNumber]
        frame, _ = cvz.putTextRect(frame, 'Total Questions: {}'.format(qTotal), [50, 50], 2, 2, colorT=(0,0,0), offset=10, border=4)
        frame, box = cvz.putTextRect(frame, mcq.question, [150, 150], 2, 2, cv.FONT_HERSHEY_SCRIPT_COMPLEX, offset=18, border=4)
        frame, box1 = cvz.putTextRect(frame, mcq.choice1, [150, 250], 2, 2, cv.FONT_HERSHEY_SIMPLEX, offset=15, border=4)
        frame, box2 = cvz.putTextRect(frame, mcq.choice2, [600, 250], 2, 2, cv.FONT_HERSHEY_SIMPLEX, offset=15, border=4)
        frame, box3 = cvz.putTextRect(frame, mcq.choice3, [150, 350], 2, 2, cv.FONT_HERSHEY_SIMPLEX, offset=15, border=4)
        frame, box4 = cvz.putTextRect(frame, mcq.choice4, [600, 350], 2, 2, cv.FONT_HERSHEY_SIMPLEX, offset=15, border=4)

        #Checking for a Hand
        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8][:2]
            cursor2 = lmList[12][:2]
            length, info  = detector.findDistance(cursor,cursor2)
    
            # To Check if the Distance between index finger and middle finger
            if length <= 30 and length >=20:
                mcq.update(cursor,[box1,box2,box3,box4])
                print(mcq.userAns)
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    quesNumber += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score/qTotal)*100,2)
        frame, _ = cvz.putTextRect(frame, 'Total No of Questions solved : {}'.format(qTotal),[350,150], 2, 2, offset=15, border=3, colorB=(130,200,255), colorT=(255,25,25))
        frame, _ = cvz.putTextRect(frame, "Your Quiz Completed ", [450, 250], 2, 2, offset=15, border=3, colorB=(130,200,255), colorT=(255,25,25))
        frame, _ = cvz.putTextRect(frame, f'Your Score: {score}%', [450, 350], 2, 2, offset=15, border=3,colorB=(130,200,255),colorT=(255,25,25))
        frame, _ = cvz.putTextRect(frame, 'Press the Q/q button to Exit', [350, 450], 2, 2, offset=15, border=3, colorB=(130,200,255), colorT=(255,25,25))

    # Draw progress bar
    Probar = 150 + (900//qTotal)*quesNumber
    #Bar Positioning
    cv.rectangle(frame,(150,600),(Probar,620),(17,171,50),cv.FILLED)
    #Progress bar width and height
    cv.rectangle(frame, (150, 600), (1050, 620), (255, 255, 255),5, cv.FILLED)
    #Display the Score in Percentage
    frame, _ = cvz.putTextRect(frame, f'{round((quesNumber/qTotal)*100)}%', [1130, 635], 2, 4, offset=16, border=5, colorT=(25,255,0),colorB=(255,255,255))

    cv.imshow("Frame",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()