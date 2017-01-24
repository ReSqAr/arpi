from PyQt5.QtCore import QUrl, QMetaObject, Qt, Q_ARG, QVariant, QModelIndex, QAbstractListModel

class AppOverviewModel(QAbstractListModel):
    def __init__(self, apps, parent=None):
        super(AppOverviewModel, self).__init__()
        self._apps = apps
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._apps)

    def data(self, index, role):
        app = self._apps[index.row()]
        
        if role == Qt.DisplayRole:
            return app.appname
        elif role == Qt.UserRole:
            return app.appid
        else:
            return QVariant()
        
    def roleNames(self):
        return {
                    Qt.DisplayRole : b"appname",
                    Qt.UserRole    : b"appid",
            }

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
        
        
        # create and set model
        appModel = AppOverviewModel(self._apps)
        self._view.rootContext().setContextProperty("appModel",appModel)
        
        # afterwards load the qml file
        self._view.setSource(self._qml)
        root = self._view.rootObject()
        
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
