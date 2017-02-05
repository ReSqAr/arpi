from PyQt5.QtCore import QCoreApplication, QUrl

translate = QCoreApplication.translate

app_name = translate("app name", "Example")
app_description = translate("app description", "Example.")



def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/example/res/example.qml'))

    #exit()
    
    print( globalconfig )
