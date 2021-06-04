import numpy as np
import cv2
import math

diametro_medido = 5.5


cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()

    limiar_inferior = np.array([100,100,100])

    limiar_superior = np.array([140,255,255])

    frameHSI = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    ImagemSegmentada = cv2.inRange(frameHSI,limiar_inferior,limiar_superior)

    contornos, __ = cv2.findContours(ImagemSegmentada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contornos = sorted(contornos, key=lambda x:cv2.contourArea(x), reverse=True)

    objeto = contornos[0]

    (x,y),raio = cv2.minEnclosingCircle(objeto)

    x = int(x)
    y = int(y)
    raio = int(raio)

    centro = (x,y)

    cv2.circle(frame,centro,raio,(0,0,255),2)

    area = cv2.contourArea(objeto)

    tamanho_pixel = ((5.5/2)/raio)*((5.5/2)/raio)

    area_medida = area*tamanho_pixel

    fonte = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    cv2.putText(frame,str(tamanho_pixel),centro,fonte,0.5,(255,255,255),2,cv2.LINE_AA)

    cv2.imshow('frame',frame)
    cv2.imshow('ImagemSegmentada',ImagemSegmentada)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()