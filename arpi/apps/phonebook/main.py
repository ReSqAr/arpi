import csv

from PyQt5.QtCore import QCoreApplication, QUrl, Qt

import arpi.lib.showlistmodel as showlistmodel


translate = QCoreApplication.translate

app_name = lambda: translate("app name", "Phonebook")
app_description = lambda: translate("app description", "Telephone numbers")


def activate( view, back, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    
    activate_here = lambda: activate( view, back, globalconfig )
    
    # create structure
    actions = [
                (
                    translate("phonebook app","Find"),
                    translate("phonebook app","Find number"),
                    lambda: activate_find(view, activate_here, globalconfig),
                ),
                (
                    translate("phonebook app","Add"),
                    translate("phonebook app","Add number"),
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
        Load the keyboard page so the user can input the contact's name.
    """
    view.setSource(QUrl('arpi/res/lib/OnScreenTextEdit/OnScreenTextEdit.qml'))
    root = view.rootObject()
    
    root.setProperty("alphabet",translate("phonebook app","ABCDEFGHIJKLMNOPQRSTUVWXYZ-"))
    root.setProperty("rowCount",3)
    root.setProperty("autoCapitalisation",True)
    root.setProperty("autoCapitalisationLetters"," -")

    root.reinitialiseKeyboard.emit()

    globalconfig.say(translate("phonebook app","Please enter the contact's name."))

    # read function
    def read(keyid):
        if keyid == "enter@OSTE":
            globalconfig.say(translate("phonebook app - OnScreenTextEdit", "Confirm:") + " " + root.property("currentText") )
        elif keyid == "backspace@OSTE":
            globalconfig.say(translate("phonebook app - OnScreenTextEdit", "Backspace"))
        elif keyid == " ":
            globalconfig.say(translate("phonebook app - OnScreenTextEdit", "Space"))
        else:
            globalconfig.say( keyid )

    # connect signals
    root.finished.connect(lambda name: activate_add_page_2(view,back,globalconfig,name), Qt.QueuedConnection)
    root.selected.connect(lambda keyid: read(keyid), Qt.QueuedConnection)
    root.back.connect(lambda: back(), Qt.QueuedConnection)

def activate_add_page_2( view, back, globalconfig, name ):
    """
        Load the keyboard page again so that the user can input the number.
    """
    view.setSource(QUrl('arpi/res/lib/OnScreenTextEdit/OnScreenTextEdit.qml'))
    root = view.rootObject()
    
    root.setProperty("alphabet",translate("numbers","1234567890"))
    root.setProperty("rowCount",2)
    root.setProperty("autoCapitalisation",False)

    root.reinitialiseKeyboard.emit()

    globalconfig.say(translate("phonebook app","Please enter the contact's telephone number."))

    # read function
    def read(keyid):
        if keyid == "enter@OSTE":
            globalconfig.say(translate("phonebook app", "Confirm:") + " " + root.property("currentText") )
        elif keyid == "backspace@OSTE":
            globalconfig.say(translate("phonebook app", "Backspace"))
        elif keyid == " ":
            globalconfig.say(translate("phonebook app", "Space"))
        else:
            globalconfig.say( keyid )

    # save contacts details
    def save(name, number):
        phonebook_path = globalconfig.configpath / 'phonebook.csv'
        with phonebook_path.open("a",newline='') as phonebook:
            writer = csv.writer(phonebook)
            writer.writerow([name,number])

    # connect signals
    root.finished.connect(lambda number: (save(name,number),back()), Qt.QueuedConnection)
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
        with phonebook_path.open("r",newline='') as phonebook:
            reader = csv.reader(phonebook)
            entries = [(row[0],row[1]) for row in reader]
    
    # nothing to show if there are no entries
    if not entries:
        globalconfig.say( translate("phonebook app","The phone book is empty."), blocking=True )
        back()
        return
    
    entries.sort(key=lambda row: row[0].lower())
    
    # setup QML
    showlistmodel.setup( view,
                            [a[0] for a in entries], # displayed text
                            lambda index: activate_show( view, activate_here, globalconfig, *entries[index]), # activation action
                            lambda index: globalconfig.say(entries[index][0]), # selection action: read name
                            back
                        )

def activate_show( view, back, globalconfig, name, number ):
    """
        Show the telephone number
    """
    view.rootContext().setContextProperty("name",name)
    view.rootContext().setContextProperty("number",number)

    view.setSource(QUrl('arpi/apps/phonebook/res/ShowNumber.qml'))
    
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
