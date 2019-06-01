import cv2 as cv

from matplotlib import pyplot as plt

img1=cv.imread("/Users/liuxiaoxu/Downloads/puzzles/cattmp1.png",0)

img2=cv.imread("/Users/liuxiaoxu/Downloads/puzzles/cat.png",0)

orb=cv.ORB_create() #创建一个orb特征检测器

kp1,des1=orb.detectAndCompute(img1,None) #计算img1中的特征点和描述符

kp2,des2=orb.detectAndCompute(img2,None) #计算img2中的

bf = cv.BFMatcher(cv.NORM_HAMMING,crossCheck=True) #建立匹配关系

mathces=bf.match(des1,des2)# 匹配描述符

mathces=sorted(mathces,key=lambda x:x.distance) #据距离来排序

img3= cv.drawMatches(img1,kp1,img2,kp2,mathces[:40],img2,flags=2) #画出匹配关系

plt.imshow(img3),plt.show() #用matplotlib描绘出来