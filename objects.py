import cv2
import numpy as np


def loadClassesNames():
        with open('dnn_model/classes.txt') as f:
            Objects = [line.replace('\n','') for line in f.readlines()]
        f.close()
        return Objects
class Object():
    All = {}
    LastID = 0
    Threshold = 50
    MaxFramesWithOutNoMove = 20
    TemporalStep = 1
    WhiteList = ["person", "car", "truck"]
    ClassesNames = loadClassesNames()
    
    @classmethod
    def create(cls, name, PosIni, rectangle):
        """
        if ID in cls.All.keys():
            raise IndexError(f"No puede existir dos ID's iguales ID: {ID}")
        
        if len(list(cls.All.keys())) >1 and ID != np.max(list(cls.All.keys())) + 1:
            txtErr = f"Los ID deben de ser consecutivos ID: {ID}"
            txtErr += f"\nSiguiente ID: {np.max(list(cls.All.keys())) + 1}"
            raise IndexError(txtErr)
        """
        object_ = Object(name, PosIni, rectangle)
        cls.All[Object.LastID] = object_
        return object_
    
    @classmethod
    def NewFrame(cls, Coords, Classes, Rectangles):
        
        for coor, class_, rectangle in zip(Coords, Classes, Rectangles):
            
            min_dis = 100
            min_dis_ID = None
            for ID in Object.All.keys():
                d = Object.All[ID].getDistance(coor)
                if d < Object.Threshold and d < min_dis and Object.All[ID].Life == True:
                    min_dis = d
                    min_dis_ID = ID
            # Si está más cerca de un objeto, se actualiza su posición
            if min_dis_ID != None and Object.areEqual(Object.All[min_dis_ID].name, Object.ClassesNames[class_]):
                Object.All[min_dis_ID].ActPosition(coor)
                Object.All[min_dis_ID].LastTemporalStep = Object.TemporalStep
            #Si no, es un objeto nuevo
            else:
                Object.create(class_, coor, rectangle)
                Object.All[Object.LastID].LastTemporalStep = Object.TemporalStep
        
        Object.TemporalStep += 1
        Object.checkDeath()
        
    
    @classmethod
    def areEqual(cls, Name1, Name2):
        D = {"car": "car", "truck": "car",  "person": "person"}
        return D[Name1] == D[Name2]
        
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
            if onlyALives and Object.All[k].Life == False:
                continue
            Diff = Object.TemporalStep - Object.All[k].LastTemporalStep
            if Diff > 5:
                continue
            
            x, y = Object.All[k].getPosition()
            cv2.putText(frame, str(Object.All[k].ID), (x ,y-7), 0,1, (0,0,255), 2)
        
    @classmethod
    def reset(cls):
        cls.All = {}
        cls.LastID = 0
        cls.TemporalStep = 1
        
    
    def __init__(self, name, PosIni, Rectangle):
        self.name = Object.ClassesNames[name]
        self.PosIni = PosIni
        self.Life = True
        self.LastTemporalStep = 1
        self.ID = Object.LastID
        self.path = [PosIni]
        self.Rectangle = Rectangle
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

