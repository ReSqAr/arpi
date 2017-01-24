from PyQt5.QtCore import QUrl

app_name = "Numbers" 
app_description = "Telephone numbers"


def activate( view, exit, configpath ):
    """
        Start the app by loading the QML file.
    """
    view.setSource(QUrl('arpi/apps/telephone/res/telephone.qml'))

    #exit()
    
    print( configpath )
