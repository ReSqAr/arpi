from PyQt5.QtCore import QUrl, QMetaObject, Qt, Q_ARG, QVariant


class Overview:
    _qml = QUrl('arpi/res/overview.qml')
    
    def __init__(self, view, apps, say):
        self._view = view
        self._apps = apps
        self._say = say
        
    def activate(self):
        self._view.setSource(self._qml)
    
        root = self._view.rootObject()

        for app in self._apps:
            QMetaObject.invokeMethod(root, "appModel_append", Qt.DirectConnection, Q_ARG(QVariant,[app.appname,app.appid]))


        root.activated.connect(lambda text: print(text))

