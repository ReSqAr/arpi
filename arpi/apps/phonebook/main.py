import os
import csv
from PyQt5.QtCore import QCoreApplication, QUrl, Qt

from arpi.lib.showlistmodel import ShowListModel

translate = QCoreApplication.translate


class App:
    app_name = lambda: translate("app name", "Phonebook")
    app_description = lambda: translate("app description", "Telephone numbers")

    def __init__(self, view, leave_app, global_config):
        """
            Start the app by loading the QML file.
        """

        # save variables
        self._view = view
        self._global_config = global_config
        self._leave_app = leave_app

    def __call__(self):
        # activate main page
        self.activate_main(self._leave_app)


    def activate_main(self, back):
        # create structure
        actions = [
            (
                translate("phonebook app", "Find"),
                translate("phonebook app", "Find number"),
                lambda: self.activate_find(lambda: self.activate_main(back)),
            ),
            (
                translate("phonebook app", "Add"),
                translate("phonebook app", "Add number"),
                lambda: self.activate_add(lambda: self.activate_main(back)),
            ),
        ]

        # delegate view to ShowListModel which lists both options (find,add)
        ShowListModel(
                        self._view,
                        # displayed text
                        [a[0] for a in actions],
                        # activation action
                        lambda index: actions[index][2](),
                        # selection action: read aloud
                        lambda index: self._global_config.say(actions[index][1]),
                        # go back to overview
                        back,
                    )()

    def activate_add(self, back):
        """
            Load the keyboard page so the user can input the contact's name.
        """
        filename = os.path.dirname(__file__) + '/../../res/lib/OnScreenTextEdit/OnScreenTextEdit.qml'
        self._view.setSource(QUrl(filename))
        root = self._view.rootObject()

        root.setProperty("alphabet", translate("phonebook app", "ABCDEFGHIJKLMNOPQRSTUVWXYZ-"))
        root.setProperty("rowCount", 3)
        root.setProperty("autoCapitalisation", True)
        root.setProperty("autoCapitalisationLetters", " -")

        root.reinitialiseKeyboard.emit()

        self._global_config.say(translate("phonebook app", "Please enter the contact's name."))

        # read function
        def read(keyid):
            if keyid == "enter@OSTE":
                self._global_config.say(
                    translate("phonebook app - OnScreenTextEdit", "Confirm:") + " " + root.property("currentText"))
            elif keyid == "backspace@OSTE":
                self._global_config.say(translate("phonebook app - OnScreenTextEdit", "Backspace"))
            elif keyid == " ":
                self._global_config.say(translate("phonebook app - OnScreenTextEdit", "Space"))
            else:
                self._global_config.say(keyid)

        # connect signals
        root.finished.connect(lambda name: self.activate_add_page_2(back, name), Qt.QueuedConnection)
        root.selected.connect(lambda keyid: read(keyid), Qt.QueuedConnection)
        root.back.connect(lambda: back(), Qt.QueuedConnection)


    def activate_add_page_2(self, back, name):
        """
            Load the keyboard page again so that the user can input the number.
        """
        filename = os.path.dirname(__file__) + '/../../res/lib/OnScreenTextEdit/OnScreenTextEdit.qml'
        self._view.setSource(QUrl(filename))
        root = self._view.rootObject()

        root.setProperty("alphabet", translate("numbers", "1234567890"))
        root.setProperty("rowCount", 2)
        root.setProperty("autoCapitalisation", False)

        root.reinitialiseKeyboard.emit()

        self._global_config.say(translate("phonebook app", "Please enter the contact's telephone number."))

        # read function
        def read(keyid):
            if keyid == "enter@OSTE":
                self._global_config.say(translate("phonebook app", "Confirm:") + " " + root.property("currentText"))
            elif keyid == "backspace@OSTE":
                self._global_config.say(translate("phonebook app", "Backspace"))
            elif keyid == " ":
                self._global_config.say(translate("phonebook app", "Space"))
            else:
                self._global_config.say(keyid)

        # save contacts details
        def save(name, number):
            phonebook_path = self._global_config.configpath / 'phonebook.csv'
            with phonebook_path.open("a", newline='') as phonebook:
                writer = csv.writer(phonebook)
                writer.writerow([name, number])

        # connect signals
        root.finished.connect(lambda number: (save(name, number), back()), Qt.QueuedConnection)
        root.selected.connect(lambda keyid: read(keyid), Qt.QueuedConnection)
        root.back.connect(lambda: back(), Qt.QueuedConnection)


    def activate_find(self, back):
        """
            Load the find page.
        """
        activate_here = lambda: self.activate_find(back)

        # load phone book
        phonebook_path = self._global_config.config_path / 'phonebook.csv'

        entries = []
        if phonebook_path.is_file():
            with phonebook_path.open("r", newline='') as phonebook:
                reader = csv.reader(phonebook)
                entries = [(row[0], row[1]) for row in reader]

        # nothing to show if there are no entries
        if not entries:
            self._global_config.say(translate("phonebook app", "The phone book is empty."), blocking=True)
            back()
            return

        entries.sort(key=lambda row: row[0].lower())

        # delegate view to ShowListModel which lists all contacts
        ShowListModel(
                        self._view,
                        # displayed text
                        [a[0] for a in entries],
                        # activation action
                        lambda index: self.activate_show(activate_here, *entries[index]),
                        # selection action: read name
                        lambda index: self._global_config.say(entries[index][0]),
                        back,
                    )()


    def activate_show(self, back, name, number):
        """
            Show the telephone number
        """
        self._view.rootContext().setContextProperty("name", name)
        self._view.rootContext().setContextProperty("number", number)

        filename = os.path.dirname(__file__) + '/res/ShowNumber.qml'
        self._view.setSource(QUrl(filename))

        def read(index):
            if index == 0:
                self._global_config.say(name)
            elif index == 1:
                self._global_config.say(" ".join(number), "slow")
            else:
                raise RuntimeError("impossible situation")

        # connect signals
        root = self._view.rootObject()
        root.activated.connect(lambda index: read(index), Qt.QueuedConnection)
        root.selected.connect(lambda index: read(index), Qt.QueuedConnection)
        root.back.connect(lambda: back(), Qt.QueuedConnection)

        # read number
        read(1)
