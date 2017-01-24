# python3-pyqt5.qtquick

import sys, pathlib
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from arpi.say.say import Say

apps = []

# load apps
from arpi.apps.weather import main as weather
apps.append(weather)
from arpi.apps.telephone import main as telephone
apps.append(telephone)

# overview app
from arpi.app_overview import Overview


# create global config

class GlobalConfig:
    def __init__(self):
        self.configpath = pathlib.Path.home() / '.config' / 'arpi'
        self.configpath.mkdir(exist_ok=True)
        
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
    say = Say(globalconfig)

    # create quick view
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    # start program
    Overview(view, apps, say, globalconfig).activate()
    view.show()

    # clean up
    mainApp.exec_()
    sys.exit()
    
