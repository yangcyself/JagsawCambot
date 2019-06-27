def DragToCorner(ply,sor_shape,img_shape,tempPos = None,ex = 0, ey = 0):
    img = ply.getOneShot()
    target = cutout_target(img)
    if(tempPos is None):
        tempPos = []
        _ = cutout_template(None,img.copy(),tempPos)
        x0,y0 = (tempPos[0] + img.shape[1]*0.114 , tempPos[1] + img.shape[0]*0.111)
    else:
        x0,y0 = tempPos
#     (x0,y0), _= matching(ply.sourceimg,img.copy(),mode = "match",debug = True)
    # shift from the corner to the middle of the template
    x0,y0 = x0+10+20, y0+30
    
#     x,y = int(img.shape[1]*0.273), int(img.shape[0]*0.120)
    x = int(ex*sor_shape[1]/5) + int(img_shape[1]*0.273)
    y = int(ey*sor_shape[0]/5) + int(img_shape[0]*0.120)
    print("###########################")
    print("DRAG TO CORNER tryOneDrag:",x0,y0,x,y,img.shape[:2])
    return ply.tryOneDrag(x0,y0,x,y,img.shape[:2],shot = True,back = False,roundAbout = (x+20,y0))
    
# img = DragToCorner(ply)

def dragToGrid(ply,x0,y0,x1,y1,sor_shape,img_shape,shot,back = True):
    """
    x,y is the cordinate of the source area 0...4
    """
    x0 = int(x0*sor_shape[1]/5 + img_shape[1]*0.273 + sor_shape[1]/10)
    y0 = int(y0*sor_shape[0]/5 + img_shape[0]*0.120 + sor_shape[0]/10)
    x1 = int(x1*sor_shape[1]/5) + int(img_shape[1]*0.273)
    y1 = int(y1*sor_shape[0]/5) + int(img_shape[0]*0.120)
    # to get to the middle of the template
#     x0,y0 = x0 +34, y0+37 # sor_shape[1]/10
    
    print("ply.tryOneDrag",x0,y0,x1,y1,img_shape[:2],shot,back)
    return ply.tryOneDrag(x0,y0,x1,y1,img_shape[:2],shot = shot,back = back)

# img = ply.getOneShot()
# sor = cutout_target(img)
# plt.imshow(sor)
# plt.show()
# dragToGrid(ply,2,2,0,0,sor.shape[:2],img.shape[:2],False)
# dragToGrid(ply,0,0,2,4,sor.shape[:2],img.shape[:2],False)


def playOneStep(ply):
    img = ply.getOneShot() # whole screen before move
    target = cutout_target(img.copy())
    
    (x0,y0), scores = old_matching(ply.sourceimg.copy(),img.copy(),mode = "match",debug = True)
    print("Template: ",x0,y0,"img shape: ", img.shape[:2])
    #应该还需要10-20的调整
    #为什么有时候会出现不停止直接走然后图像出现异常的情况
    possible = findEmpty(ply.emptyimg,target,mode = "debug")
    ey = np.argmax(scores)//5 
    ex = np.argmax(scores)%5
    while(not possible[ey][ex]):
        scores[ey][ex] = -1
        ey = np.argmax(scores)//5 
        ex = np.argmax(scores)%5
    moved_template = DragToCorner(ply,target.shape[:2],img.shape[:2],(x0,y0),ex,ey) # screen after the template is moved to corner
    
    template = find_template(moved_template,img,ex,ey)
    plt.imshow(template)
    plt.show()
    source = cutout_target(ply.sourceimg)
#     global tmpcount
#     cv2.imwrite("tmpTemplate%d.png"%tmpcount,template)
#     cv2.imwrite("tmpSource%d.png"%tmpcount,source)
#     tmpcount += 1
    scores = matching(source,template)
#     print("Rx,RY",rx,ry)
#     rx,ry = min(4,rx),min(4,ry)
#     rx,ry = int(rx),int(ry)
#     scores = matching(ply.sourceimg,moved_template,img,mode = "match",debug = True)
#     scores[ry][rx] = 99999999
    initial_num = possible.sum()
    print("possible:", possible)
    print("scores:",scores)
#     ex,ey = 0,0 # the point to check the correctness
    scores[ey][ex] = -1
    triedCount = 0
    while(possible.sum()>0):
        y = np.argmax(scores)//5 # x => i 
        x = np.argmax(scores)%5
        print("DRAG TO: ",x,y)
        scores[y][x]=-1
        if(not possible[y][x] ): # we don't have to move to 0,0, we just check it in the next round
            continue
        possible[y][x] = False
        
        timg = dragToGrid(ply,ex,ey,x,y,target.shape[:2],img.shape[:2],shot=True, back = False)
        timg = cutout_target(timg)
#         print("Tries To Drag:",x0,y0,x,y)
        
        triedCount += 1
        
        plt.imshow(timg)
        plt.show()
        empty = findEmpty(ply.emptyimg,timg,mode = "debug")
        print("TRIED:", triedCount )
        if(not empty[ey][ex] or empty[y][x]):
            break
        ex,ey = x,y
playOneStep(ply)