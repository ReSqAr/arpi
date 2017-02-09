from PyQt5.QtCore import QCoreApplication, QUrl

translate = QCoreApplication.translate

app_name = lambda: translate("app name", "Example")
app_description = lambda: translate("app description", "Example.")



def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/example/res/example.qml'))

    #exit()
    
    print( globalconfig )
