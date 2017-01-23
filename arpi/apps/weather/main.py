from PyQt5.QtCore import QUrl

appname = "Weather" 
appid = "weather"



def activate( view, exit, configpath ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/weather/res/weather.qml'))

    #exit()
    
    print( configpath )
