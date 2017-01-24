from PyQt5.QtCore import QUrl

app_name = "Weather" 
app_description = "Weather forecast"



def activate( view, exit, configpath ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/weather/res/weather.qml'))

    #exit()
    
    print( configpath )
