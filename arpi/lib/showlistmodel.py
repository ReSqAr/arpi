from PyQt5.QtCore import QUrl, Qt, Q_ARG, QStringListModel


def setup( view, string_list, activated, selected, back ):
    """
        Creates a string list model and loads it in QML,
        the functions activated and selected get called
        accordingly.
    """
    # clear view
    view.setSource(QUrl(''))

    # create and attach model
    listModel = QStringListModel( string_list )
    view.rootContext().setContextProperty("listModel",listModel)

    # afterwards load the qml file
    view.setSource(QUrl('arpi/res/lib/ListModel.qml'))
    root = view.rootObject()

    # if an element is activated, load the appropriate app
    # IMPORTANT: to avoid crashes, we use a QueuedConnection
    root.activated.connect(lambda index: activated(index), Qt.QueuedConnection)

    # handle selection change
    root.selected.connect(lambda index: selected(index), Qt.QueuedConnection)

    # handle back
    if back:
        root.back.connect(lambda: back(), Qt.QueuedConnection)
    
    # trigger initial selection event
    selected(0)
    
