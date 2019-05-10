#ifndef USRSERVER
#define  USRSERVER

#include "stdafx.h"
#include "usrGameController.h"
//#include <QObject>
#pragma comment(lib,"ws2_32.lib") //Winsock Library

class usrServer : public QObject
{
	Q_OBJECT;
private:
	usrGameController* controller;


public:
	usrServer(usrGameController* GC);
	~usrServer();

public slots:
	void ServerRun();
};

#endif