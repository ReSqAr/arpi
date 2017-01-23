# python3-pyqt5.qtquick

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from arpi.say.say import say

apps = []

# load apps
from arpi.apps.weather import main as weather
apps.append(weather)

# overview app
from arpi.app_overview import Overview



mainApp = QApplication(sys.argv)

# create quick view
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)

Overview(view, apps, say).activate()
view.show()

mainApp.exec_()
sys.exit()
 
