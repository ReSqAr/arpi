from PyQt5.QtCore import QCoreApplication, QUrl

translate = QCoreApplication.translate

app_name = "empty"
app_description = "empty"



def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/empty/res/empty.qml'))

    #exit()
    
    print( globalconfig )
