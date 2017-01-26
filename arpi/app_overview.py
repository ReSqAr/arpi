import arpi.lib.showlistmodel as showlistmodel

class Overview:
    
    def __init__(self, view, apps, globalconfig):
        self._view = view
        self._apps = apps
        self._globalconfig = globalconfig
        
    def activate(self):
        """
            Create and show a list model.
        """
        # create
        appList = [app.app_name for app in self._apps]
        
        # setup QML
        showlistmodel.setup( self._view, appList, self.load_app, self.read_description, None )
        
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
        self._globalconfig.say( self._apps[app_index].app_description )
