# -^- coding:utf-8 -^-
import cv2
import matplotlib.pyplot as plt
import numpy as np
import re
from Cut import *

def RGBEqualizeHist(target):
    for i in range(3):
        target[:,:,i] = cv2.equalizeHist(target[:,:,i])
    return target

def cutout_source(source,template):
    source = RGBEqualizeHist(source)
    #sAx = int(source.shape[1]*0.470)
    #sAy = int(source.shape[0]*0.343)
    #sBx = int(source.shape[1]*0.641)
    #sBy = int(source.shape[0]*0.667)
    sAx = int(template.shape[1]*0.273)
    sAy = int(template.shape[0]*0.120)
    sBx = int(template.shape[1]*0.735)
    sBy = int(template.shape[0]*0.895)

    source = source[sAy:sBy,sAx:sBx,:]
    return source

def cutout_template_area(source,template):
    template = RGBEqualizeHist(template)
    #tAx = int(template.shape[1]*0.172)
    #tAy = int(template.shape[0]*0.144)
    #tBx = int(template.shape[1]*0.250)
    #tBy = int(template.shape[0]*0.799)
    #114
    #0.111
    #201
    #790
    tAx = int(template.shape[1]*0.114)
    tAy = int(template.shape[0]*0.111)
    tBx = int(template.shape[1]*0.201)
    tBy = int(template.shape[0]*0.850)
    temp = template[tAy:tBy,tAx:tBx,:]
    return temp

def cutout_template(source,template,temp_pos = None):
    temp = cutout_template_area(source,template)
    gradient = get_Gradient(temp)
    #高斯平滑&阈值分割
    blurred = cv2.blur(gradient, (5, 5))
    _, thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)
    # image,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=cv2.contourArea, reverse=True)
    if(temp_pos is None): # display mode
        out = temp.copy()
        for i in range(min(5,len(contours))):
            t = temp.copy()
            c = contours[i]
            x,y,w,h= cv2.boundingRect(c)
            cv2.rectangle(t,(x,y),(x+w,y+h),(0,255,0),2)
            out = np.concatenate([out,t],axis = 1)
        return out
    else:
        c = contours[0]
        x,y,w,h= cv2.boundingRect(c)
        out = temp[y:y+w,x:x+w]
        temp_pos.append(x)
        temp_pos.append(y)
        # draw a bounding box arounded the detected barcode and display the image
        return out

def cutout_target(template):
    #DAx = int(template.shape[1]*0.303)
    #DAy = int(template.shape[0]*0.123)
    #DBx = int(template.shape[1]*0.696)
    #DBy = int(template.shape[0]*0.889)
    DAx = int(template.shape[1]*0.273)
    DAy = int(template.shape[0]*0.120)
    DBx = int(template.shape[1]*0.735)
    DBy = int(template.shape[0]*0.895)
    target = template[DAy:DBy,DAx:DBx,:]
    return target

def generateGaussianKernel(shape,u,cov):
    res = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            p = np.array((i,j))
            deltaS = np.sum((p-u)**2)
            res[i][j] = np.exp(-deltaS/cov)
    return res

def old_matching(source,template,mode="match",debug = False):
    sor = cutout_source(source,template)
    
    s_x = int(sor.shape[0]/5)
    s_y = int(sor.shape[1]/5)
    
    temp_area = cutout_template_area(source,template)
    
    temp_pos = []
    temp = cutout_template(source,template,temp_pos)
    #change 
    
    temp_pos = (temp_pos[0],temp_pos[1]) # change it into tuple 
    tep = cv2.copyMakeBorder(temp,10,40,10,40,cv2.BORDER_CONSTANT,value=[0,0,0])
    
    scores = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            img = sor[s_x*i:s_x*(i+1),s_y*j:s_y*(j+1),:]
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR_NORMED) #87.29 vs 85.55
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR) # 不好，倒数
            # res = cv2.matchTemplate(tep,img,cv2.TM_CCOEFF) # 最高！
            res = cv2.matchTemplate(tep,img,cv2.TM_CCOEFF_NORMED) # 最高！！！
#             res = cv2.matchTemplate(tep,img,cv2.TM_SQDIFF) # 不好
#             res = cv2.matchTemplate(tep,img,cv2.TM_SQDIFF_NORMED) # 最高，但是和后面的差距并不很大
            g = generateGaussianKernel(res.shape,np.array([15,15]),500)
            res = res * g
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            scores[i,j] = max_val

    if(debug or mode!="match"): 
        source_x = np.argmax(scores)//5 # x => i 
        source_y = np.argmax(scores)%5
        source_x *= s_x
        source_y *= s_y

        source_y += temp_area.shape[1]
        
        out = np.zeros( (max(temp_area.shape[0],sor.shape[0]),
                            temp_area.shape[1]+sor.shape[1] ,3),dtype = np.uint8)
        out[0:temp_area.shape[0],0:temp_area.shape[1] ,:] = temp_area
        out[0:sor.shape[0],temp_area.shape[1]:,:] = sor
        
        cv2.line(out, temp_pos, (source_y+20,source_x+20), (0,255,0), 2) #line point: (shape1, shape0)

    if(mode=="match"):
        temp_pos = (temp_pos[0] + template.shape[1]*0.114 , temp_pos[1] + template.shape[0]*0.111) # add the temp area margin
        if(debug):
            plt.imshow(out)
            plt.show()
        return temp_pos, scores
    else:
        return out

def findEmpty(emptypic, targetpic,threshold = 100, mode = "release"):    
    tx,ty,_ = targetpic.shape
    target = cv2.cvtColor(targetpic, cv2.COLOR_BGR2GRAY)
    (_, tar) = cv2.threshold(target, 90, 255, cv2.THRESH_BINARY)

    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    er = cv2.erode(tar,kernel1,iterations = 1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    fgmask = cv2.morphologyEx(er, cv2.MORPH_CLOSE, kernel2,iterations=3)
    
    if(mode=="debug"):
        plt.imshow(fgmask)
        plt.show()
    # cut it to be dividedable by 3 //5
    w,h = fgmask.shape
    fgmask = fgmask[:(w//5)*5,:(h//5)*5]
    wd,hd = int(fgmask.shape[0]/5),int(fgmask.shape[1]/5)  # the width and height eash small block
    fgmask = fgmask.reshape((5,wd,5,hd))
    fgmask = fgmask.mean(axis = 3)
    fgmask = fgmask.mean(axis = 1)
    print(fgmask)
    return fgmask<threshold
