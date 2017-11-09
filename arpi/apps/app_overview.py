from arpi.lib.showlistmodel import ShowListModel


class AppOverview:
    def __init__(self, view, apps, global_config):
        self._view = view
        self._apps = apps
        self._global_config = global_config

    def activate(self):
        """
            Create and show a list model.
        """
        # create
        app_name_list = [app.app_name() for app in self._apps]

        # delegate view to ShowListModel which lists all loaded_apps
        ShowListModel(
                        self._view,
                        app_name_list,
                        self.load_app,
                        self.read_app_description,
                        None
                    )()

    def load_app(self, app_index):
        """
            Load the app.
        """
        print("DEBUG: loading: '{}'".format(self._apps[app_index].app_name()))
        app = self._apps[app_index](self._view, self.activate, self._global_config)
        app()

    def read_app_description(self, app_index):
        """
            Read the description of the given app.
        """
        self._global_config.say(self._apps[app_index].app_description())
