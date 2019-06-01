import numpy as np
import cv2 as cv
import math as m

class SAD:
    #初始化，wsize为窗口大小，disp为视差等级
    def __init__(self , *args):
        if len(args) == 0:
            self.wsize = 3
            self.disp = 20
        elif len(args)!=2:
            print("argument error!")
        else:
            self.wsize,self.disp = args

    #生成高斯模板
    def getGaussKernel(self,sigma):
        gaussMatrix = np.zeros((self.wsize,self.wsize),np.float)

        cH = (self.wsize - 1)/2
        cW = (self.wsize - 1)/2

        for r in range(self.wsize):
            for c in range(self.wsize):
                dis = m.pow(r-cH,2) + m.pow(c-cW,2)
                gaussMatrix[r,c] = m.exp(-dis/(2*m.pow(sigma,2)))
        sumG = np.sum(gaussMatrix)
        gaussKernel = gaussMatrix/sumG

        return gaussKernel

    #生成均值模板
    def getMeanKernel(self):
        meanKernel = np.ones((self.wsize,self.wsize))
        meanKernel = meanKernel/np.sum(meanKernel)
        return meanKernel

    #滤波器
    def weightfil(self,img):
        w, h, ch = img.shape
        pad = self.wsize // 2
        eximg = np.zeros((w + pad*2, h + pad*2, ch), img.dtype)
        #周围补0
        eximg[pad:w + pad, pad:h + pad, :] = img
        print("hahha{}".format(eximg[3:6,2:8,1]))

        result = np.zeros((w, h, ch), np.uint8)
        #根据不同的模板进行滤波
        #kernel = self.getMeanKernel()
        kernel = self.getGaussKernel(1.6)
        print("kernel = {}".format(kernel))
        #彩色图像各通道
        for c in range(ch):
            for i in range(pad,w+pad):
                for j in range(pad,h+pad):
                    img_w = eximg[i-pad:i+pad+1,j-pad:j+pad+1,c]
                    result[i-pad][j-pad][c] = np.sum(img_w*kernel)
        print("filter done!")
        return result

    def computeSAD(self, imgL, imgR):
        w,h,c = imgL.shape
        pad = self.wsize//2
        #图像周围填充
        eximgL = np.zeros((w+pad*2,h+pad*2,c),imgL.dtype)
        eximgR = np.zeros((w+pad*2,h+pad*2,c),imgR.dtype)
        eximgL[pad:w+pad,pad:h+pad,:]=imgL
        eximgR[pad:w+pad,pad:h+pad,:]=imgR
        #转为灰度图
        eximgL = cv.cvtColor(eximgL,cv.COLOR_RGB2GRAY)
        eximgR = cv.cvtColor(eximgR,cv.COLOR_RGB2GRAY)
        cv.imshow("leftimg",eximgL)
        cv.imshow("rightimg",eximgR)


        #计算代价矩阵
        costMat = np.zeros((w,h,self.disp))
        print(costMat.shape)
        for d in range(self.disp):
            for wi in range(pad,w+pad):
                for hj in range(pad,h+pad):
                    if(hj+d>=h+pad):
                        costMat[wi-pad,hj-pad,d] = 0
                    else:
                        winL = eximgL[wi-pad:wi+pad+1,hj-pad+d:hj+pad+1+d]
                        winR = eximgR[wi-pad:wi+pad+1,hj-pad:hj+pad+1]
                        winDif = winR.astype(np.int16) - winL.astype(np.int16)
                        costMat[wi-pad,hj-pad,d] = np.sum(abs(winDif))

        #视差选择
        dispmap = np.zeros((w,h),np.uint8)
        for i in range(w):
            for j in range(h):
                cost_d = costMat[i,j,:]
                dispmap[i,j] = list(cost_d).index(min(cost_d))

        #视差图显示
        xmax = dispmap.max()
        xmin = dispmap.min()
        reg_disp = np.zeros((w,h),np.uint8)
        for i in range(w):
            for j in range(h):
                reg_disp[i,j] =round(255*(dispmap[i,j]-xmin)/(xmax-xmin))
        cv.imshow("disparity",reg_disp)


print(cv.__version__)
#生成实例SAD参数为0个或2个
#0个时，默认窗口大小为3，视差大小为20
#2个时，第一个参数为窗口大小（为奇数），第二个参数为视差大小
sad = SAD(5,30)
imgL = cv.imread("col3.png",1)
imgR = cv.imread("col5.png")
sad.computeSAD(imgL,imgR)

img_Guass = sad.weightfil(imgL)
cv.imshow("Guass".encode("gbk").decode(errors="ignore"),img_Guass)
cv.waitKey()
