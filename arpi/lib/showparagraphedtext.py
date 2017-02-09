from PyQt5.QtCore import QUrl, Qt, Q_ARG, QStringListModel


def setup( view, paragraph_list, activated, selected, back ):
    """
        Export the string list to the QML
        and make sure that the signals activated and selected
        get called accordingly.
    """
    # clear view
    view.setSource(QUrl(''))

    # attach string list
    view.rootContext().setContextProperty("paragraphList",paragraph_list)

    # afterwards load the qml file
    view.setSource(QUrl('arpi/res/lib/ParagraphedText.qml'))
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
    
