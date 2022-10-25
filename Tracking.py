#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import numpy as np
from object_detection import ObjectDetection


# In[31]:


YOLO = ObjectDetection()


# In[34]:


def loadClassesNames():
        with open('dnn_model/classes.txt') as f:
            Objects = [line.replace('\n','') for line in f.readlines()]
        f.close()
        return Objects


# In[195]:


class Object():
    All = {}
    LastID = 0
    Threshold = 20
    MaxFramesWithOutNoMove = 10
    TemporalStep = 1
    ClassesNames = loadClassesNames()
    
    @classmethod
    def create(cls, name, PosIni):
        """
        if ID in cls.All.keys():
            raise IndexError(f"No puede existir dos ID's iguales ID: {ID}")
        
        if len(list(cls.All.keys())) >1 and ID != np.max(list(cls.All.keys())) + 1:
            txtErr = f"Los ID deben de ser consecutivos ID: {ID}"
            txtErr += f"\nSiguiente ID: {np.max(list(cls.All.keys())) + 1}"
            raise IndexError(txtErr)
        """
        object_ = Object(name, PosIni)
        cls.All[Object.LastID] = object_
        return object_
    
    @classmethod
    def NewFrame(cls, Coords, Classes):
        
        for coor, class_ in zip(Coords, Classes):
            min_dis = 100
            min_dis_ID = None
            for ID in Object.All.keys():
                d = Object.All[ID].getDistance(coor)
                if d < Object.Threshold and d < min_dis and Object.All[ID].Life == True:
                    min_dis = d
                    min_dis_ID = ID
            # Si está más cerca de un objeto, se actualiza su posición
            if min_dis_ID != None and Object.All[min_dis_ID].name == Object.ClassesNames[class_]:
                Object.All[min_dis_ID].ActPosition(coor)
                Object.All[min_dis_ID].LastTemporalStep = Object.TemporalStep
            #Si no, es un objeto nuevo
            else:
                Object.create(class_, coor)
                Object.All[Object.LastID].LastTemporalStep = Object.TemporalStep
        
        Object.TemporalStep += 1
        Object.checkDeath()
        
    @classmethod
    def ShowAll(cls, onlyALives = False):
        for k in Object.All.keys():
            if onlyALives:
                if Object.All[k].Life == False:
                    continue
                    
            print(" ================================== ")
            print(f"ID: {Object.All[k].ID}")
            print(f"Tipo: {Object.All[k].name}")
            print(f"Path: {Object.All[k].path}")
            print(f"Pos: {Object.All[k].getPosition()}")
            print(" ================================== ")
            print()
            
    @classmethod
    def checkDeath(cls):
        
        for ID in Object.All.keys():
            Diff = Object.TemporalStep - Object.All[ID].LastTemporalStep
            if Diff > Object.MaxFramesWithOutNoMove:
                Object.All[ID].Life = False
                print(f"Murió ID = {ID}")
                
    @classmethod
    def PutID(cls, frame):
        onlyALives = True
        for k in Object.All.keys():
            if onlyALives:
                if Object.All[k].Life == False:
                    continue
            
            x,y = Object.All[k].getPosition()
            cv2.putText(frame, str(Object.All[k].ID), (x ,y-7), 0,1, (0,0,255), 2)
        
    
    def __init__(self, name, PosIni):
        self.name = Object.ClassesNames[name]
        self.PosIni = PosIni
        self.Life = True
        self.LastTemporalStep = 1
        self.ID = Object.LastID
        self.path = [PosIni]
        Object.LastID += 1
        
    def ActPosition(self, ActPos):
        self.path.append(ActPos)
    
    def getPosition(self):
        return self.path[-1]
    
    def checkMove(self):
        """
        Si un objeto permanece inmovil por más de n frames,
        se considera como muerto
        """
        pass
        #if len(self.path) > 10:
            
            
    
    def getDistance(self, Pos):
        return np.sqrt((Pos[0] - self.getPosition()[0])**2 +                       (Pos[1] - self.getPosition()[1])**2)


# In[197]:


cap = cv2.VideoCapture('videos/short.mp4')
nFrame = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    
    key = cv2.waitKey(0)
    
    (class_ids, scores, boxes) = YOLO.detect(frame)
    for box, class_id in zip(boxes, class_ids):
        (x, y, w, h) = box
        cv2.rectangle(frame, (x,y), (x + w, y + h), (255,0,0),2)
        cx = int((x + x + w)/2)
        cy = int((y + y + h)/2)
        cv2.circle(frame, (cx,cy), 5, (0,0,255), -1 )
        
        if nFrame% 5 == 0:
            Object.NewFrame([[cx,cy]], [class_id])
        
        Object.PutID(frame)
        
    if nFrame% 5 == 0:
        Object.ShowAll(onlyALives = True)
    
    cv2.imshow("Frame", frame)
    if key == 27:
        break  
    
    nFrame += 1
        
cap.release()
cv2.destroyAllWindows()


# In[170]:


Object.NewFrame([[20.4,10.4]], [3])


# In[171]:


Object.ShowAll(onlyALives=True)


# In[24]:


f.close()


# In[67]:


np.array(Object.All[1].path[-5:])


# In[180]:


x,y = Object.All[1].getPosition()


# In[181]:


x,y


# In[ ]:


# Para una nueva versión, eliminarlos en lugar de matarlos en código
# del Object.All[ID]
# Pero antes revisar a donde se han ido
# detección cada n frames

