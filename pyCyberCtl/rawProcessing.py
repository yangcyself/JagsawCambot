# -^- coding: utf-8 -^-
from numpy.linalg import inv
import cv2
import numpy as np

kernel = cv2.imread("pics/kernel.png")
MaxDeltaThreshold = 10
MatchPairsNumber = 10

def solving(kp1,kp2,matches):
    X = []
    Y = []
    for m in matches:
        p1 = kp1[m.queryIdx]
        p2 = kp2[m.trainIdx]
        X.append((*(p1.pt),1))
        Y.append(p2.pt)
    maxDelta = 150
    # 由于不可避免的误差，需要把误判的去掉再求解
    while(maxDelta > MaxDeltaThreshold and len(X)>6):
        X_ = np.array(X)
        Y_ = np.array(Y)
        B = inv((X_.T.dot(X_))).dot(X_.T).dot(Y) 
        Y_ = X_.dot(B)
        deltaY =  abs(Y_ - Y)
        maxY = np.argmax(np.max(deltaY,axis=1))
        maxDelta = np.max(deltaY)
        print(maxY)
        del(X[maxY])
        del(Y[maxY])
    return B

def TurnWindow(img):
    """
    思路： 先找配对的点，
    这些点可以看作是由一个仿射矩阵生成的，可以通过这些点解出背后的仿射矩阵
    """
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img,None)

    kp2, des2 = orb.detectAndCompute(kernel,None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)

    B = solving(kp1,kp2,matches[:MatchPairsNumber])

    rows,cols = img.shape[:2]
    dst = cv2.warpAffine(img,B.T,(cols,rows))
    return dst