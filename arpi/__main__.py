# python3-pyqt5.qtquick

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from arpi.say.say import say

apps = []

# load apps
from arpi.apps.weather import main as weather
apps.append(weather)


from arpi import app_overview



mainApp = QApplication(sys.argv)

# create quick view
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)

app_overview.init(view, apps, say)
view.show()

mainApp.exec_()
sys.exit()
 
