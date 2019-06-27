import numpy as np
import cv2 
import matplotlib.pyplot as plt
from matchUtil import cutout_target

def find_template(img,empty,y,x):
    img = cutout_target(img)
    s_x = img.shape[0]/5
    s_y = img.shape[1]/5
    return img[ int(s_x*x+ s_x/4)       :   int(s_x*(x+1) - s_x/4) ,
                int(s_y * y + s_x/4)    :   int(s_y*(y+1) - s_x/4) , :]

def matching(source, template):
    h, w = template.shape[:2]# rows->h, cols->w
    hs, ws = source.shape[:2]
    s_x = int(source.shape[0]/5)
    s_y = int(source.shape[1]/5)
    #loc = np.array(range(2))
    # 相关系数匹配方法：cv2.TM_CCOEFF
    bd = (30,30) # border
    source = cv2.copyMakeBorder(source,0,bd[0],0,bd[1],cv2.BORDER_CONSTANT,value=[0,0,0])
    scores = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            img = source[s_x*i:s_x*(i+1)+bd[0],s_y*j:s_y*(j+1)+bd[1],:]
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR_NORMED) #87.29 vs 85.55
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR) # 不好，倒数
            # res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF) # 最高！
            res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED) # 最高！！！
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            scores[i][j] = max_val
    # res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # # left_top = max_loc  # 左上角
    # # right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    # # #cv.rectangle(source, left_top, right_bottom, 255, 2)
    # # #return left_top
    # # loc = [0,0]
    # # loc[0] = left_top[0] + h/2
    # # loc[1] = left_top[1] + w/2
    # # hsd=hs//5
    # # wsd=ws//5
    # # loc[0]=loc[0]//hsd
    # # loc[1]=loc[1]//wsd
    # return loc
    return scores



