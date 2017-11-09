import os
from PyQt5.QtCore import QCoreApplication, QUrl
#from PyQt5.QtWebEngineWidgets import QWebEngineView # python3-pyqt5.qtwebengine

from OpenGL import GL  #Linux workaround.  See: http://goo.gl/s0SkFl

translate = QCoreApplication.translate

app_name = lambda: translate("app name", "Call")
app_description = lambda: translate("app description", "Call a contact.")


def activate( view, back, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    
    #activate_here = lambda: activate( view, back, globalconfig )

    globalconfig.config['call']['url']


    filename = os.path.dirname(__file__) + '/res/webrtc.qml'
    view.setSource(QUrl(filename))
