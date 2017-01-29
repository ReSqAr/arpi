import csv

from PyQt5.QtCore import QCoreApplication, QUrl, Qt, Q_ARG

import arpi.lib.showlistmodel as showlistmodel


translate = QCoreApplication.translate

app_name = translate("app name", "Numbers")
app_description = translate("app description", "Telephone numbers")


def activate( view, back, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    
    activate_here = lambda: activate( view, back, globalconfig )
    
    # create structure
    actions = [
                (
                    translate("telephone app","Find"),
                    translate("telephone app","Find number"),
                    lambda: activate_find(view, activate_here, globalconfig),
                ),
                (
                    translate("telephone app","Add"),
                    translate("telephone app","Add number"),
                    lambda: activate_add(view, activate_here, globalconfig),
                ),
            ]
        
    # setup QML
    showlistmodel.setup( view,
                            [a[0] for a in actions], # displayed text
                            lambda index: actions[index][2](), # activation action
                            lambda index: globalconfig.say(actions[index][1]), # selection action: read aloud
                            back,
                        )

def activate_add( view, back, globalconfig ):
    """
        Load the add page.
    """
    view.setSource(QUrl('arpi/res/lib/OnScreenTextEdit/OnScreenTextEdit.qml'))
    root = view.rootObject()
    
    root.setProperty("alphabet",translate("alphabet","ABCDEFGHIJKLMNOPQRSTUVWXYZ-"))
    root.setProperty("rowCount",3)
    root.setProperty("autoCapitalisation",True)
    root.setProperty("autoCapitalisationLetters"," -")

    root.reinitialiseKeyboard.emit()

    # read function
    def read(keyid):
        if keyid == "enter@OSTE":
            globalconfig.say(translate("OnScreenTextEdit", "Confirm:") + " " + root.property("currentText") )
        elif keyid == "backspace@OSTE":
            globalconfig.say(translate("OnScreenTextEdit", "Backspace"))
        elif keyid == " ":
            globalconfig.say(translate("OnScreenTextEdit", "Space"))
        else:
            globalconfig.say( keyid )

    # connect signals
    root.finished.connect(lambda text: globalconfig.say(text), Qt.QueuedConnection)
    root.selected.connect(lambda keyid: read(keyid), Qt.QueuedConnection)
    root.back.connect(lambda: back(), Qt.QueuedConnection)

def activate_find( view, back, globalconfig ):
    """
        Load the find page.
    """
    activate_here = lambda: activate_find( view, back, globalconfig )

    # load phonebook
    phonebook_path = globalconfig.configpath / 'phonebook.csv'
    
    entries = []
    if phonebook_path.is_file():
        with phonebook_path.open("r") as phonebook:
            reader = csv.DictReader(phonebook)
            entries = [(row[0],row[1]) for row in reader]
    
    # nothing to show if there are no entries
    if not entries:
        globalconfig.say( translate("telephone app","The phone book is empty."), blocking=True )
        back()
        return
        
    # setup QML
    showlistmodel.setup( view,
                            [a[0] for a in entries], # displayed text
                            lambda index: activate_show( view, activate_here, globalconfig, *entries[index]), # activation action
                            lambda index: globalconfig.say(entries[index][0]), # selection action: read name
                            back
                        )

def activate_show( view, back, globalconfig, name, number ):
    """
        Load the show page.
    """
    view.rootContext().setContextProperty("name",name)
    view.rootContext().setContextProperty("number",number)

    view.setSource(QUrl('arpi/apps/telephone/res/ShowNumber.qml'))
    
    def read(index):
        if index == 0:
            globalconfig.say(name)
        elif index == 1:
            globalconfig.say(number, "slow")
        else:
            raise RuntimeError("impossible situation")
    
    # connect signals
    root = view.rootObject()
    root.activated.connect(lambda index: read(index), Qt.QueuedConnection)
    root.selected.connect(lambda index: read(index), Qt.QueuedConnection)
    root.back.connect(lambda: back(), Qt.QueuedConnection)
    
    # read number
    read(1)
