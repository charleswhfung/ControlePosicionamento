import numpy as np
import cv2

cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

#HSI -> hue matiz, Saturation saturacao, I Intensity brilho
#Cor/Limite inferior/Limite superior
#Amarelo/10,100,100/50,255,255
#Azul/100,100,100/140,255,255
#Verde/40,100,100/80,255,255
#Vermelho/160,100,100/200,255,255


while(True):
    ret, frame = cap.read()

    limiar_inferior = np.array([100,100,100])

    limiar_superior = np.array([140,255,255])

    frameHSI = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    ImagemSegmentada = cv2.inRange(frameHSI,limiar_inferior,limiar_superior)

    contornos, __ = cv2.findContours(ImagemSegmentada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contornos = sorted(contornos, key=lambda x:cv2.contourArea(x), reverse=True)

    m=0
    x1=0
    y1=0
    x2=0
    y2=0

    for c in contornos:
        m=m+1
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        momento = cv2.moments(c)

        cx = momento["m10"] / momento["m00"]
        cy = momento["m01"] / momento["m00"]

        cx = int(cx)
        cy = int(cy)

        STR = "("+str(cx)+","+str(cy)+")" #(100,200)

        cv2.putText(frame,STR,(cx,cy),font,0.5,(0,0,255),2,cv2.LINE_AA)

        centro = (cx,cy)
        raio = 5
        cv2.circle(frame,centro,raio,(0,255,0),-1)
        if m==1:
            x1=cx
            y1=cy
        if m==2:
            x2=cx
            y2=cy
            break


    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow('frame',frame)

    cv2.imshow('Segmentada',ImagemSegmentada)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.realease()
cv2.destroyAllWindows