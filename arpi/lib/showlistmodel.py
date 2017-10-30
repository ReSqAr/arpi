from PyQt5.QtCore import QUrl, Qt


def setup( view, string_list, activated, selected, back ):
    """
        This function uses the view to display the string_list
        in a QML ListView, additionally the signals activated
        and selected are connected to the given functions and
        the escape key triggers a function call to back.
    """
    # clear view
    view.setSource(QUrl(''))

    # attach string list
    view.rootContext().setContextProperty("stringList",string_list)

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
    
