#include "stdafx.h"
#include "usrServer.h"

#define	BUF_SIZE	1024
#define USVPORT		19876

/*
using MS
*/

// usrServer::usrServer(usrGameController* GC)
// {
// 	controller = GC;
// 	qDebug() << "Server online.";
	
// }

// usrServer::~usrServer()
// {
// }


// void usrServer::ServerRun()
// {

// 	WSADATA wsd;
// 	int iRet = 0;

// 	// 初始化套接字动态库
// 	if (WSAStartup(MAKEWORD(2, 2), &wsd) != 0) {
// 		printf("WSAStartup failed:%d!\n", WSAGetLastError());
		
// 	}

// 	SOCKET socketSrv = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
// 	SOCKADDR_IN addrSrv;
// 	SOCKADDR_IN addrClient;
// 	char strRecv[BUF_SIZE] = { 0 }, strSend[BUF_SIZE] = "udp server send";
// 	int len = sizeof(SOCKADDR);

// 	// 设置服务器地址
// 	ZeroMemory(strRecv, BUF_SIZE);
// 	addrSrv.sin_addr.s_addr = INADDR_ANY;
// 	//addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
// 	addrSrv.sin_family = AF_INET;
// 	addrSrv.sin_port = htons(PORT_);

// 	// 绑定套接字
// 	iRet = bind(socketSrv, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));
// 	if (SOCKET_ERROR == iRet)
// 	{
// 		printf("bind failed%d!\n", WSAGetLastError());
// 		closesocket(socketSrv);
// 		WSACleanup();
// 	}

// 	// 从客户端接收数据
// 	printf("udp server start...\n");
// 	while (TRUE)
// 	{
// 		iRet = recvfrom(socketSrv, strRecv, BUF_SIZE, 0, (SOCKADDR*)&addrClient, &len);
// 		if (SOCKET_ERROR == iRet) {
// 			printf("recvfrom failed !\n");
// 			closesocket(socketSrv);
// 			WSACleanup();
			
// 		}

// 		printf("Recv From Client:%s\n", strRecv);

// 		// 向客户端发送数据
// 		sendto(socketSrv, strSend, sizeof(strSend), 0, (SOCKADDR*)&addrClient, len);
// 	}

// 	closesocket(socketSrv);
// 	WSACleanup();

// }

/* 
Using QT udp
*/


usrServer::usrServer(usrGameController* GC) :
	QObject(0)
{
	controller = GC;
	// create a QUDP socket
	socket = new QUdpSocket(this);

	// The most common way to use QUdpSocket class is 
	// to bind to an address and port using bind()
	// bool QAbstractSocket::bind(const QHostAddress & address, 
	//     quint16 port = 0, BindMode mode = DefaultForPlatform)
	socket->bind(QHostAddress::LocalHost, USVPORT);

	connect(socket, SIGNAL(readyRead()), this, SLOT(readyRead()));
}


void usrServer::readyRead()
{
	// when data comes in
	QByteArray buffer;
	buffer.resize(socket->pendingDatagramSize());

	QHostAddress sender;
	quint16 senderPort;

	// qint64 QUdpSocket::readDatagram(char * data, qint64 maxSize, 
	//                 QHostAddress * address = 0, quint16 * port = 0)
	// Receives a datagram no larger than maxSize bytes and stores it in data. 
	// The sender's host address and port is stored in *address and *port 
	// (unless the pointers are 0).

	socket->readDatagram(buffer.data(), buffer.size(),
		&sender, &senderPort);

	if (senderPort == USVPORT)
		return;

	qDebug() << "Message from: " << sender.toString();
	qDebug() << "Message port: " << senderPort;
	qDebug() << "Message: " << buffer;

	//QByteArray Data;

	//Data.append("Hello from UDP");
	//socket->writeDatagram(Data, QHostAddress::LocalHost, senderPort);


	QByteArray datagram;
	QDataStream out(&datagram, QIODevice::WriteOnly);
	out.setVersion(QDataStream::Qt_4_3);
	out << "Hello From Server";

	socket->writeDatagram(datagram, QHostAddress::LocalHost, senderPort);
}