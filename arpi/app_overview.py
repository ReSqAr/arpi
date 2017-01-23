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

        root.activated.connect(lambda appid: self.load_app(appid), Qt.QueuedConnection)

    def load_app(self, appid):
        print("loading:", appid)
        
        for app in self._apps:
            if app.appid == appid:
                app.activate( self._view, self.activate )
                break
        else:
            raise RuntimeError("impossible situation")
