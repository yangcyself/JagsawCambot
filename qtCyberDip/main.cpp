#include "qtcyberdip.h"
//#include "usrServer.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	qtCyberDip w;
	w.show();
	return a.exec();
}
