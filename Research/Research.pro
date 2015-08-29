#-------------------------------------------------
#
# Project created by QtCreator 2015-03-04T18:00:48
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Research
TEMPLATE = app


SOURCES += main.cpp\
        research.cpp

HEADERS  += research.h

FORMS    += research.ui \
    interface.ui \
    widgetsforviz.ui \
    datasetviewer.ui \
    screeshot.ui

DISTFILES += \
    Research.qml \
    ResearchForm.ui.qml
