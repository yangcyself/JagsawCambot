import numpy as np
import cv2 
import matplotlib.pyplot as plt


def find_template(img,empty,x,y):
    DAx = int(empty.shape[1]*0.273)
    DAy = int(empty.shape[0]*0.120)
    #250,100
    DBx = int(empty.shape[1]*0.735)
    DBy = int(empty.shape[0]*0.895)
    target_cut = img[DAy-int(empty.shape[1]*0.023):DBy,DAx-int(empty.shape[0]*0.01):DBx,:]
    empty_cut = empty[DAy-int(empty.shape[1]*0.023):DBy,DAx-int(empty.shape[0]*0.01):DBx,:]
    #w,h,_ = target_cut.shape
    w,h = DBy-DAy,DBx-DAx
    target = target_cut[int(x*(w//5)):int(x*(w//5))+int(w*1.5)//5,int(y*(h//5)):int(y*(h//5))+int(h*1.5)//5,:]
    empty = empty_cut[int(x*(w//5)):int(x*(w//5))+int(w*1.5)//5,int(y*(h//5)):int(y*(h//5))+int(h*1.5)//5,:]
    #empty = empty_cut[:int(w*1.5)//5,:int(h*1.5)//5,:]
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    empty_gray = cv2.cvtColor(empty, cv2.COLOR_BGR2GRAY)
    sub = target_gray - empty_gray
    sub_ = target - empty
    (_, sub_bin) = cv2.threshold(sub,30, 255, cv2.THRESH_BINARY)
    #+ cv2.THRESH_OTSU)
    #30
    
    plt.imshow(sub_bin)
    plt.show()
    
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    er = cv2.erode(sub_bin,kernel1,iterations = 2)


    image, contours, hierarchy = cv2.findContours(er,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    width = rect[1][0]
    height = rect[1][1]
    if width < height:
        width,height = height,width
        
    
    center = np.mean(box,axis = 0)

    cut = target[int(center[1]-height/2):int(center[1]+height/2),int(center[0]-width/2):int(center[0]+width/2)]
    x,y,_ = cut.shape
    if x<=25 or y<=25:
        #target_cut = img[DAy:DBy,DAx:DBx,:]

        return target_cut[int(x*(w//5))+int(w*0.03)-20:int(x*(w//5))+int(w*1.1)//5+20,
                          int(y*(h//5))+int(h*0.04)-20:int(y*(h//5))+int(h*1.1)//5+20,:]
    plt.imshow(cut)
    plt.show()
    
    
    return cut


def matching(source, template):
    h, w = template.shape[:2]# rows->h, cols->w
    hs, ws = source.shape[:2]
    #loc = np.array(range(2))
    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    #cv.rectangle(source, left_top, right_bottom, 255, 2)
    #return left_top
    loc = [0,0]
    loc[0] = left_top[0] + h/2
    loc[1] = left_top[1] + w/2
    hsd=hs//5
    wsd=ws//5
    loc[0]=loc[0]//hsd
    loc[1]=loc[1]//wsd
    return loc



