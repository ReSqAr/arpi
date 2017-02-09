from PyQt5.QtCore import QCoreApplication, QUrl

import arpi.lib.mail
import arpi.lib.showlistmodel as showlistmodel
import arpi.lib.showparagraphedtext as showparagraphedtext

translate = QCoreApplication.translate

app_name = lambda: translate("app name", "EMail")
app_description = lambda: translate("app description", "Read emails.")



def activate( view, exit, globalconfig ):
    """
        Start the app by loading the QML file.
    """
    activate_here = lambda: activate( view, exit, globalconfig )
    
    globalconfig.say( translate("email app","Loading emails.") )
    
    try:
        host = globalconfig.config['email']['host']
        username = globalconfig.config['email']['username']
        password = globalconfig.config['email']['password']
        
        print( "DEBUG: host: {}".format(host) )
        print( "DEBUG: username: {}".format(username) )
        print( "DEBUG: password: {}".format(len(password)) )

        account = arpi.lib.mail.Account(host, username, password)
        messages = account.get_messages(10)
    except:
        globalconfig.say( translate("email app","Retrieving emails failed."), blocking=True )
        exit()
        return
        
    # nothing to show if there are no emails
    if not messages:
        globalconfig.say( translate("email app","There are no emails to display."), blocking=True )
        exit()
        return
    
    # sort
    messages.sort(key=lambda message: message.get_datetime(), reverse=True)
    
    # prepare arguments for showlistmodel
    displayed_text = []
    for msg in messages:
        subject = msg.get_subject()
        sender = msg.get_sender()
        text = translate("email app (display)", "{sender}: {subject}").format(subject=subject,sender=sender)
        displayed_text.append( text )
    
    def activation_action(index):
        activate_show( view, activate_here, globalconfig, messages[index] )
    
    def selection_action(index):
        msg = messages[index]
        subject = msg.get_subject()
        sender = msg.get_sender()
        text = translate("email app (tts)", "{sender}: {subject}").format(subject=subject,sender=sender)
        globalconfig.say( text )
    
    # setup QML
    showlistmodel.setup( view, displayed_text, activation_action, selection_action, exit )
    
    
def activate_show( view, back, globalconfig, message ):
    """
        Show the gallery
    """
    print( "DEBUG: showing email: {}".format(message) )
    
    
    text = message.get_text()
    print( "DEBUG: text:" )
    print( text )
    
    lines = text.split('\n')
    lines = [line.strip().strip("> \t") for line in lines]
    
    
    # create list of paragraphs
    paragraphs = []
    current_paragraph = []
    for line in lines:
        if not line:
            # 'flush' current paragraph
            if current_paragraph:
                paragraphs.append( ' '.join(current_paragraph) )
                current_paragraph = []
        else:
            # add to current paragraph
            current_paragraph.append( line )
    # commit last paragraph
    if current_paragraph:
        paragraphs.append( ' '.join(current_paragraph) )
    
    
    # add information
    sender = message.get_sender()
    text = translate("email app", "From: {sender}").format(sender=sender)
    paragraphs.insert( 0, text )

    subject = message.get_subject()
    text = translate("email app", "Subject: {subject}").format(subject=subject)
    paragraphs.insert( 1, text )
    
    # setup QML
    showparagraphedtext.setup( view,
                                paragraphs,
                                lambda index: globalconfig.say(paragraphs[index]),
                                lambda index: globalconfig.say(paragraphs[index]),
                                back
                            )
    
