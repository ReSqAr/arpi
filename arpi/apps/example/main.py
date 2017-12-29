import os
from PyQt5.QtCore import QCoreApplication, QUrl
import PyQt5.QtWebEngineWidgets  # KEEP IT! https://bugreports.qt.io/browse/QTBUG-46720

translate = QCoreApplication.translate


class App:
    app_name = lambda: translate("app name", "Example")
    app_description = lambda: translate("app description", "Example.")

    def __init__(self, view, leave_app, global_config):
        """
            Initialise the app
        """
        # save a variables
        self._view = view
        self._global_config = global_config
        self._leave_app = leave_app

    def __call__(self):
        """
            Start the app by loading the QML file
        """
        self.activate_main(self._leave_app)

    def activate_main(self, back):
        # clear view
        self._view.setSource(QUrl(''))

        filename = os.path.dirname(__file__) + '/res/example.qml'
        self._view.setSource(QUrl(filename))
        root = self._view.rootObject()

        # connect signals
        #root.back.connect(lambda: back(), Qt.QueuedConnection)

        print(self._global_config)
