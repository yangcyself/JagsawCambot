import numpy as np 
import cv2
import matplotlib.pyplot as plt

#可能会用到的空洞填充
def fillHole(im_in):
    im_floodfill = im_in.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_in.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    im_out = im_in | im_floodfill_inv

    return im_out

#旋转
def rotate(img,center,angle):
    rows,cols,channel = img.shape
    print(angle)
    #if(angle <= -87):
    #angle = angle + 90
    M = cv2.getRotationMatrix2D((center[0],center[1]),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
   
    return dst


def get_Gradient(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    return gradient


def get_Contour(img):
    #边缘
    gradient = get_Gradient(img)
    #高斯平滑&阈值分割
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)

    #检测并画出轮廓
    # image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    # draw a bounding box arounded the detected barcode and display the image
    cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
    #cv2.imshow("Image", img)

    #cv2.imwrite("contoursImage2.jpg", image)
    #cv2.waitKey(0)

    #旋转
    width = rect[1][0]
    height = rect[1][1]
    angle = rect[2]
    if width < height:
        width,height = height,width
        angle = angle + 90
        
    
    center = np.mean(box,axis = 0)
    r = rotate(img,center,angle)
    #cv2.imshow("rotate", r)
    #cv2.waitKey(0)

    #裁剪

    cut = r[int(center[1]-height/2):int(center[1]+height/2),int(center[0]-width/2):int(center[0]+width/2)]
    # cv2.imshow("cut", cut)
    # cv2.waitKey(0)
    return cut






