from PyQt5.QtCore import QUrl, Qt, Q_ARG, QStringListModel

class Overview:
    _qml = QUrl('arpi/res/overview.qml')
    
    def __init__(self, view, apps, say, globalconfig):
        self._view = view
        self._apps = apps
        self._say = say
        self._globalconfig = globalconfig
        
    def activate(self):
        """
            Load the QML document, populate the model and connect the signals.
        """
        
        # create and set model
        appModel = QStringListModel([app.app_name for app in self._apps])
        self._view.rootContext().setContextProperty("appModel",appModel)
        
        # afterwards load the qml file
        self._view.setSource(self._qml)
        root = self._view.rootObject()
        
        # if an element is activated, load the appropriate app
        # IMPORTANT: to avoid crashes, we use a QueuedConnection
        root.activated.connect(lambda app_index: self.load_app(app_index), Qt.QueuedConnection)

        # handle selection change
        root.selected.connect(lambda app_index: self.read_description(app_index), Qt.QueuedConnection)

    def load_app(self, app_index):
        """
            Load the app.
        """
        print("DEBUG: loading: '{}'".format(self._apps[app_index].app_name))
        self._apps[app_index].activate( self._view, self.activate, self._globalconfig )

    def read_description(self, app_index):
        """
            Read the description of the given app.
        """
        self._say( self._apps[app_index].app_description )
