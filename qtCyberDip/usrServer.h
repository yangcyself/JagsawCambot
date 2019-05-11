#ifndef USRSERVER
#define  USRSERVER

#include "stdafx.h"
#include "usrGameController.h"

/*
using MS
*/

//#include <QObject>
// #pragma comment(lib,"ws2_32.lib") //Winsock Library

// class usrServer : public QObject
// {
// 	Q_OBJECT;
// private:
// 	usrGameController* controller;


// public:
// 	usrServer(usrGameController* GC);
// 	~usrServer();

// public slots:
// 	void ServerRun();
// };

// #endif

/*
using QT udp
*/


// myudp.h


#include <QObject>
#include <QUdpSocket>
#include <QDataStream>

class usrServer : public QObject
{
	Q_OBJECT
public:
	explicit usrServer(usrGameController* GC = nullptr);

signals:

public slots:
	void readyRead();

private:
	QUdpSocket *socket;
	usrGameController* controller;

};

#endif // MYUDP_H