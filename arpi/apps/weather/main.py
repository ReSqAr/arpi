from PyQt5.QtCore import QUrl

appname = "Weather" 
appid = "weather"



def activate( view, exit ):
    print("loading")
    view.setSource(QUrl('arpi/apps/weather/res/weather.qml'))
    print("loaded")
    #exit()
