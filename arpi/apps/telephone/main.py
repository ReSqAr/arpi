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
    pass



def activate_find( view, back, globalconfig ):
    """
        Load the find page.
    """
    activate_here = lambda: activate_find( view, back, globalconfig )

    # create structure
    numbers = [
                (
                    "Alice",
                    "00123456789"
                ),
                (
                    "Bob",
                    "00123456789"
                ),
            ]
        
    # setup QML
    showlistmodel.setup( view,
                            [a[0] for a in numbers], # displayed text
                            lambda index: activate_show( view, activate_here, globalconfig, *numbers[index]), # activation action
                            lambda index: globalconfig.say(numbers[index][0]), # selection action: read name
                            back
                        )

def activate_show( view, back, globalconfig, name, number ):
    """
        Load the add page.
    """
    pass
