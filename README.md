# qtCyberDIP
![CyberDIP](/pic/CyberDIP.png)

CyberDIP driver for windows in C++ 11.
**Original project** [qtCyberDip](https://github.com/LostXine/qtCyberDIP)


### 我们是参加“数字图像处理基础”的同学，注意:

为了方便代码评阅，建议只修改 [usrGameController.h](/qtCyberDip/usrGameController.h) 和 [usrGameController.cpp](/qtCyberDip/usrGameController.cpp) 两个文件，最后使用git提交代码。

但是由于整个QT程序的逻辑是事件驱动，usrGameController里面定义的函数processing在每一帧摄像机输入图片都被调用一遍，所以难以实现自己玩游戏的逻辑。或者说要实现机器人自己玩游戏的主动动作，只改这两个文件基本是不可能的。同时为了方便开发，我们改了[qtcyberdip.h](/qtCyberDip/qtcyberdip.h) 和 [qtcyberdip.cpp](/qtCyberDip/qtcyberdip.cpp) 两个文件.增加了简单的UDPserver功能，这样使用python就可以轻松和机器人交互。



