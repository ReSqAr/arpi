# python3-pyqt5.qtquick

import sys, pathlib
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


# create config path
configpath = pathlib.Path.home() / '.config' / 'arpi'
configpath.mkdir(exist_ok=True)

say = Say(configpath)

# create the application
mainApp = QApplication(sys.argv)

# create quick view
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)

# start program
Overview(view, apps, say, configpath).activate()
view.show()

# clean up
mainApp.exec_()
sys.exit()
 
