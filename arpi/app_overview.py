from PyQt5.QtCore import QUrl, QMetaObject, Qt, Q_ARG, QVariant


def init(view, apps, say):
    view.setSource(QUrl('arpi/res/overview.qml'))
 
    root = view.rootObject()
    print(root)

    for app in apps:
        QMetaObject.invokeMethod(root, "appModel_append", Qt.DirectConnection, Q_ARG(QVariant,[app.appname,app.appid]))

    root.activated.connect(lambda text: print(text))

