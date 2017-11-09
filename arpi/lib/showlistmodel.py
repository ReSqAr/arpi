import os

from PyQt5.QtCore import QUrl, Qt


class ShowListModel:
    def __init__(self, view, string_list, activated, selected, back=None):
        """
            This function uses the view to display the string_list
            in a QML ListView, additionally the signals activated
            and selected are connected to the given functions and
            the escape key triggers a function call to back.
        """
        self._view = view
        self._string_list = string_list
        self._activated = activated
        self._selected = selected
        self._back = back

    def __call__(self):
        # clear view
        self._view.setSource(QUrl(''))

        # attach string list
        self._view.rootContext().setContextProperty("stringList",self._string_list)

        # afterwards load the qml file
        filename = os.path.dirname(__file__) + '/../res/lib/ListModel.qml'
        self._view.setSource(QUrl(filename))
        root = self._view.rootObject()

        # if an element is activated, load the appropriate app
        # IMPORTANT: to avoid crashes, we use a QueuedConnection
        root.activated.connect(lambda index: self._activated(index), Qt.QueuedConnection)

        # handle selection change
        root.selected.connect(lambda index: self._selected(index), Qt.QueuedConnection)

        # handle back
        if self._back:
            root.back.connect(lambda: self._back(), Qt.QueuedConnection)

        # trigger initial selection event
        self._selected(0)


