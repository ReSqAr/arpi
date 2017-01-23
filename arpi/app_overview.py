from PyQt5.QtCore import QUrl, QMetaObject, Qt, Q_ARG, QVariant


class Overview:
    _qml = QUrl('arpi/res/overview.qml')
    
    def __init__(self, view, apps, say, configpath):
        self._view = view
        self._apps = apps
        self._say = say
        self._configpath = configpath
        
    def activate(self):
        """
            Load the QML document, populate the model and connect the signals.
        """
        
        self._view.setSource(self._qml)
        root = self._view.rootObject()
        
        # populate the model using a javascript function
        for app in self._apps:
            QMetaObject.invokeMethod(root, "appModel_append", Qt.DirectConnection, Q_ARG(QVariant,[app.appname,app.appid]))

        # if an element is activated, load the appropriate app
        # IMPORTANT: to avoid crashes, we use a QueuedConnection
        root.activated.connect(lambda appid: self.load_app(appid), Qt.QueuedConnection)

    def load_app(self, appid):
        """
            We try to find and load the app with the corresponding app id.
        """
        print("loading:", appid)
        
        for app in self._apps:
            if app.appid == appid:
                app.activate( self._view, self.activate, self._configpath )
                break
        else:
            raise RuntimeError("impossible situation")
