#ifndef RESEARCH_H
#define RESEARCH_H

#include <QMainWindow>

namespace Ui {
class Research;
}

class Research : public QMainWindow
{
    Q_OBJECT

public:
    explicit Research(QWidget *parent = 0);
    ~Research();

private:
    Ui::Research *ui;
};

#endif // RESEARCH_H
