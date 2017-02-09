# python3-pyqt5.qtquick

import sys, pathlib
import configparser

from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from arpi.lib.say import Say

apps = []

# load apps
from arpi.apps.phonebook import main as phonebook
apps.append(phonebook)
from arpi.apps.gallery import main as gallery
apps.append(gallery)

# overview app
from arpi.app_overview import Overview


# create global config

class GlobalConfig:
    def __init__(self):
        self.configpath = pathlib.Path.home() / '.config' / 'arpi'
        self.configpath.mkdir(exist_ok=True)
        
        self.config = configparser.ConfigParser()
        self.config.read( str(self.configpath / 'config.ini') )
        
        self.locale = QLocale.system().name()
        print("DEBUG: locale:", self.locale)
        
        self.language = self.locale[0:2]
        print("DEBUG: language", self.language)

if __name__ == '__main__':
    # create the application
    mainApp = QApplication(sys.argv)

    # create config
    globalconfig = GlobalConfig()

    # internationalisation
    # see http://doc.qt.io/qt-5/internationalization.html
    # see http://pyqt.sourceforge.net/Docs/PyQt5/i18n.html
    
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
    
