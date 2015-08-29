#include "research.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Research w;
    w.show();

    return a.exec();
}
