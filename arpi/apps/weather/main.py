from PyQt5.QtCore import QCoreApplication, QUrl

translate = QCoreApplication.translate

app_name = translate("app name", "Weather")
app_description = translate("app description", "Weather forecast")



def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/weather/res/weather.qml'))

    #exit()
    
    print( globalconfig )
