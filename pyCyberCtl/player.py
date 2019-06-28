from CyClient import *
import time
import numpy as np
from matchUtil import *
from Cut import *
import matplotlib.pyplot as plt
from findTemplate import *
PHONESIZE = (160,245)
class Player:
    def __init__(self,cli):
        self.cli = cli
        self.basePoint = np.array([0,0])
        self.sourceimg = None # the image of the jagsaw to recover
        self.emptyimg = None # the image of the empty target area 
    def setBase(self):
        # move to where 0,0 point should be in the figure
        curr = self.cli.getPos()
        print("current position: ", curr[:2])
        self.basePoint = np.array(curr[:2])
        
    def moveto(self,x,y):
        x += self.basePoint[0]
        y += self.basePoint[1]
        x,y = int(x),int(y)
        cx,cy,_  =self.cli.getPos()
        self.cli.takAction(1,x,y)
         # getPos can not get the current pos, but the target pos
        # the time is 2.76s to move from -10,-10 to 100,100
        speed = 56
        dist = ((x-cx)**2+(y-cy)**2)**(1/2)
        waittime = dist/speed + 0.5
        time.sleep(waittime)
        
        
    def movetoImg(self,x,y,imgshape,diviceShape = PHONESIZE):
        # imgshape is (y_shape, x_shape)
        '''
        x =  (1-x/imgshape[1]) * diviceShape[0] # because x is converted
        y =  y/imgshape[0] * diviceShape[1]
        '''
        x =  (1-x/imgshape[1]) * diviceShape[1] # because x is converted
        y =  y/imgshape[0] * diviceShape[0]
        x,y = y,x
        self.moveto(x,y)
    
    def retreat(self):
        #self.moveto(-10,-10)
        cx,cy,_  =self.cli.getPos()
        if(cy - self.basePoint[0] < 137):
            self.moveto(-10,-10)
        else:
            self.moveto(-10,255)

#         self.cli.takAction(3,0,0)
    
    def clickAtImg(self, x, y,imgshape,diviceShape = PHONESIZE):
        print(imgshape,diviceShape)
        self.movetoImg(x, y,imgshape,diviceShape)
#         time.sleep(2)
#         self.cli.takAction(2,0,0)
        self.cli.takAction(4,0,0)
        time.sleep(0.5)
        self.cli.takAction(3,0,0)
        self.retreat()
    
    def dragAtImg(self, x0,y0,x1,y1,imgshape,diviceShape = PHONESIZE,roundAbout = None):
        self.movetoImg(x0,y0,imgshape,diviceShape)
        self.cli.takAction(4,0,0)
#         time.sleep(0.2)
        if(roundAbout is not None):
            x2,y2 = roundAbout
            self.movetoImg(x2,y2,imgshape,diviceShape)
        self.movetoImg(x1,y1,imgshape,diviceShape)
        self.cli.takAction(3,0,0)
    
    def tryOneDrag(self,x0,y0,x1,y1,imgshape,diviceShape = PHONESIZE, shot = False, back = True, roundAbout = None):
        # drag the piece to the position and then drag it back
        # if it is the correct piece it will stay there
#         targetShape = 
        # roundAbout is the point first drag to
        sx = int(imgshape[1]*(0.735-0.273)/10) # the shift amount
        sy = int(imgshape[0]*(0.895-0.120)/10)
#         print("shot:",shot,"back",back)
        self.dragAtImg(x0,y0,x1-sx*1.25,y1+sy,imgshape,PHONESIZE,roundAbout)
        if(shot):
            self.retreat()
#             time.sleep(0.5)
            img = self.getOneShot()
            if(not back):
                return img
#         else:
#             time.sleep(2)
        #self.dragAtImg(x1,y1+30,x0,y0-30,imgshape,diviceShape = PHONESIZE)
        self.dragAtImg(x1+sx,y1+sy,x0-2*sx,y0,imgshape,diviceShape = PHONESIZE) # Note the x,y = y,x in movetoImg
        self.retreat()
        if(shot):
            return img
        
    def getOneShot(self):
        img = self.cli.getPic()
        img = get_Contour(img)
        return img
    
    def initGame(self):
        # The phone should be before the game start
        self.retreat()
        img = self.getOneShot()
        #source ?
        self.sourceimg = img
        y,x = img.shape[:2]
        #x,y = x*0.502,y*0.237
        y,x = x*0.4,y*0.84
        self.clickAtImg(x,y,img.shape[:2])
        img = self.getOneShot()
        self.emptyimg = cutout_target(img)
    def DragToCorner(self,sor_shape,img_shape,tempPos = None,ex = 0, ey = 0):
        img = self.getOneShot()
        target = cutout_target(img)
        if(tempPos is None):
            tempPos = []
            _ = cutout_template(None,img.copy(),tempPos)
            x0,y0 = (tempPos[0] + img.shape[1]*0.114 , tempPos[1] + img.shape[0]*0.111)
        else:
            x0,y0 = tempPos
        # shift from the corner to the middle of the template
        x0,y0 = x0+10+20, y0+30
        x = int(ex*sor_shape[1]/5) + int(img_shape[1]*0.273)
        y = int(ey*sor_shape[0]/5) + int(img_shape[0]*0.120)
        
        return self.tryOneDrag(x0,y0,x,y,img.shape[:2],shot = True,back = False,roundAbout =( (x+20,y0) if x==0 else None ))
    
    def dragToGrid(self,x0,y0,x1,y1,sor_shape,img_shape,shot,back = True):
        """
        x,y is the cordinate of the source area 0...4
        """
        x0 = int(x0*sor_shape[1]/5 + img_shape[1]*0.273 + sor_shape[1]/10)
        y0 = int(y0*sor_shape[0]/5 + img_shape[0]*0.120 + sor_shape[0]/10)
        x1 = int(x1*sor_shape[1]/5) + int(img_shape[1]*0.273)
        y1 = int(y1*sor_shape[0]/5) + int(img_shape[0]*0.120)
        # print("self.tryOneDrag",x0,y0,x1,y1,img_shape[:2],shot,back)
        return self.tryOneDrag(x0,y0,x1,y1,img_shape[:2],shot = shot,back = back)

    def playOneStep(self):
        img = self.getOneShot() # whole screen before move
        target = cutout_target(img.copy())

        (x0,y0), scores = old_matching(self.sourceimg.copy(),img.copy(),mode = "match",debug = False)
        scores += np.random.random((5,5))/5
        print("Template: ",x0,y0,"img shape: ", img.shape[:2])
        possible = findEmpty(self.emptyimg,target,mode = "release")
        
        trustworthy = findEmpty(target,self.emptyimg,mode = "release")
        
        ey = np.argmax(scores)//5 
        ex = np.argmax(scores)%5
        while(not possible[ey][ex]):
            scores[ey][ex] = -1
            ey = np.argmax(scores)//5 
            ex = np.argmax(scores)%5
        print("###EX,EY####",ex,ey)
        moved_template = self.DragToCorner(target.shape[:2],img.shape[:2],(x0,y0),ex,ey) # screen after the template is moved to corner
    #     global tmpcount
    #     cv2.imwrite("tmpMovedTemplate%d.png"%tmpcount,moved_template)
    #     cv2.imwrite("tmpSourceImg%d.png"%tmpcount,img)
    #     tmpcount += 1    
        template = find_template(moved_template,img,ex,ey)
        source = cutout_target(self.sourceimg)
        scores = matching(source,template)
        initial_num = possible.sum()
        print("possible:", possible)
        print("scores:",scores)
    #     ex,ey = 0,0 # the point to check the correctness
        scores[ey][ex] = -1
        triedCount = 0
        lastshot = moved_template
        while(possible.sum()>0):
            y = np.argmax(scores)//5 # x => i 
            x = np.argmax(scores)%5
            print("DRAG TO: ",x,y)
            scores[y][x]=-1
            if(not possible[y][x] and trustworthy[y][x] ):
                continue
            possible[y][x] = False

            timg = self.dragToGrid(ex,ey,x,y,target.shape[:2],img.shape[:2],shot=True, back = False)
            timg = cutout_target(timg)
    #         print("Tries To Drag:",x0,y0,x,y)

            triedCount += 1

            empty = findEmpty(self.emptyimg,timg,mode = "release")
            print("TRIED:", triedCount )
            while(empty[y][x] and empty[ey][ex]):
                # Might lose the template during the drag
                losttemplate = compareChanged(lastshot,timg,mode = "release")
                if(losttemplate is None): # the template is not detectable by find empty
                    break
                else:
                    print("LOSTED :")
                    find = compareChanged(lastshot,timg,mode = "debug")
                    plt.imshow(find)
                    plt.show()
                    dx,dy,dw,dh = losttemplate
                    dx = dx+dw/2-30
                    dy = dy + dh/2 - 30
                    timg = self.DragToCorner(target.shape[:2],img.shape[:2],(dx,dy),x,y)
                    lastshot = timg
            if((not empty[ey][ex] and trustworthy[ey][ex])or empty[y][x]):
                break
            ex,ey = x,y
            lastshot = timg
        

        

if __name__ == "__main__":
    cli = Client()
    cli.sayHello()
    ply = Player(cli)
    cli.takAction(1,10,10)
    ply.setBase()
    ply.retreat()
    ply.initGame()
    for i in range(25):
        ply.playOneStep()