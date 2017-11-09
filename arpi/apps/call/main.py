import os
from PyQt5.QtCore import QCoreApplication, QUrl
import PyQt5.QtWebEngineWidgets # https://bugreports.qt.io/browse/QTBUG-46720

translate = QCoreApplication.translate

class App:
    app_name = lambda: translate("app name", "Call")
    app_description = lambda: translate("app description", "Call a contact.")

    def __init__(self, view, leave_app, global_config):
        """
            Start the app by loading the QML file.
        """
        # save a variables
        self._view = view
        self._global_config = global_config
        self._leave_app = leave_app

    def __call__(self):
        # activate main page
        self.activate_main(self._leave_app)

    def activate_main(self, back):
        self._global_config.config['call']['url']

        filename = os.path.dirname(__file__) + '/res/webrtc.qml'
        self._view.setSource(QUrl(filename))
