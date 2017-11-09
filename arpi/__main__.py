# python3-pyqt5.qtquick

import configparser
import pathlib
import sys

from PyQt5.QtCore import QLocale, QTranslator
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication
import PyQt5.QtWebEngineWidgets # https://bugreports.qt.io/browse/QTBUG-46720

from arpi.lib.say import Say

apps = []

# load apps
from arpi.apps.phonebook import main as phonebook
apps.append(phonebook)

from arpi.apps.gallery import main as gallery
apps.append(gallery)

from arpi.apps.email import main as email
apps.append(email)

from arpi.apps.newspaper import main as newspaper
apps.append(newspaper)

from arpi.apps.call import main as call
apps.append(call)

# overview app
from arpi.app_overview import Overview


class GlobalConfig:
    """
        central configuration class
    """

    def __init__(self):
        self.configpath = pathlib.Path.home() / '.config' / 'arpi'
        self.configpath.mkdir(exist_ok=True)

        self.config = configparser.ConfigParser()
        self.config.read(str(self.configpath / 'config.ini'))

        self.locale = QLocale.system().name()
        print("DEBUG: locale:", self.locale)

        self.language = self.locale[0:2]
        print("DEBUG: language", self.language)


if __name__ == '__main__':
    # create the application
    mainApp = QApplication(sys.argv)

    # internationalisation
    # see http://doc.qt.io/qt-5/internationalization.html
    # see http://pyqt.sourceforge.net/Docs/PyQt5/i18n.html
    translator = QTranslator()
    translator.load("arpi/res/i18n/arpi_" + QLocale.system().name())
    mainApp.installTranslator(translator)

    # create config
    globalconfig = GlobalConfig()

    # create speech output class
    globalconfig.say = Say(globalconfig)

    # create quick view
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    # start program
    Overview(view, apps, globalconfig).activate()
    view.show()

    # clean up
    mainApp.exec_()
    sys.exit()
