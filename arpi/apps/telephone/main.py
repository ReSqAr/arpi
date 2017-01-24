from PyQt5.QtCore import QCoreApplication, QUrl

translate = QCoreApplication.translate

app_name = translate("app name", "Numbers")
app_description = translate("app description", "Telephone numbers")


def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/telephone/res/telephone.qml'))

    #exit()
    
    print( globalconfig )
