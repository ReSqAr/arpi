# python3-pyqt5.qtquick

import configparser
import pathlib
import sys

from PyQt5.QtCore import QLocale, QTranslator
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication

from arpi.lib.say import Say

# load apps
from arpi.apps.app_overview import AppOverview
from arpi.apps.app_loader import loaded_apps


class GlobalConfig:
    """
        central configuration class
    """

    def __init__(self):
        self.config_path = pathlib.Path.home() / '.config' / 'arpi'
        self.config_path.mkdir(exist_ok=True)

        self.config = configparser.ConfigParser()
        self.config.read(str(self.config_path / 'config.ini'))

        self.locale = QLocale.system().name()
        print("DEBUG: locale:", self.locale)

        self.language = self.locale[0:2]
        print("DEBUG: language", self.language)


def create_main_app():
    # create the application
    main_app = QApplication(sys.argv)

    # internationalisation
    # see http://doc.qt.io/qt-5/internationalization.html
    # see http://pyqt.sourceforge.net/Docs/PyQt5/i18n.html
    translator = QTranslator()
    translator.load("arpi/res/i18n/arpi_" + QLocale.system().name())
    main_app.installTranslator(translator)

    # create config
    global_config = GlobalConfig()

    # create speech output class
    global_config.say = Say(global_config)

    # create quick view
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    # start program
    AppOverview(view, loaded_apps, global_config).activate()
    view.show()

    # clean up
    main_app.exec_()
    sys.exit()


if __name__ == '__main__':
    create_main_app()
