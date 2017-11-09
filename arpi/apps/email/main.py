from PyQt5.QtCore import QCoreApplication

import arpi.lib.mail
from arpi.lib.showlistmodel import ShowListModel
from arpi.lib.showparagraphedtext import ShowParagraphedText


translate = QCoreApplication.translate

class App:
    app_name = lambda: translate("app name", "EMail")
    app_description = lambda: translate("app description", "Read emails.")

    def __init__(self, view, leave_app, global_config):
        """
            Show the last x emails.
        """
        # save variables
        self._view = view
        self._global_config = global_config
        self._leave_app = leave_app

    def __call__(self):
        # activate main page
        self.activate_main(self._leave_app)

    def activate_main(self, back):
        self._global_config.say(translate("email app", "Loading emails."))

        try:
            host = self._global_config.config['email']['host']
            username = self._global_config.config['email']['username']
            password = self._global_config.config['email']['password']

            print("DEBUG: host: {}".format(host))
            print("DEBUG: username: {}".format(username))
            print("DEBUG: password: {}".format(len(password)))

            account = arpi.lib.mail.Account(host, username, password)
            messages = account.get_messages(10)
        except:
            self._global_config.say(translate("email app", "Retrieving emails failed."), blocking=True)
            self._leave_app()
            return

        # nothing to show if there are no emails
        if not messages:
            self._global_config.say(translate("email app", "There are no emails to display."), blocking=True)
            self._leave_app()
            return

        # sort
        messages.sort(key=lambda message: message.get_datetime(), reverse=True)

        # prepare arguments for ShowListModel
        displayed_text = []
        for msg in messages:
            subject = msg.get_subject()
            sender = msg.get_sender()
            text = translate("email app (display)", "{sender}: {subject}").format(subject=subject, sender=sender)
            displayed_text.append(text)

        def activation_action(index):
            self.activate_show(lambda: self.activate_main(back), messages[index])

        def selection_action(index):
            msg = messages[index]
            subject = msg.get_subject()
            sender = msg.get_sender()
            text = translate("email app (tts)", "{sender}: {subject}").format(subject=subject, sender=sender)
            self._global_config.say(text)

        # delegate view to ShowListModel which lists all emails
        ShowListModel(
                        self._view,
                        displayed_text,
                        activation_action,
                        selection_action,
                        back,
                    )()


    def activate_show(self, back, message):
        """
            Show the email
        """
        text = message.get_text()
        print("DEBUG: showing email:")
        print(text)

        # split into lines, remove '>'
        lines = text.split('\n')
        lines = [line.strip().strip("> \t") for line in lines]

        # create list of paragraphs (between paragraphs is an empty line)
        paragraphs = []
        current_paragraph = []
        for line in lines:
            if not line:
                # 'flush' current paragraph
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
            else:
                # add to current paragraph
                current_paragraph.append(line)
        # commit last paragraph
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))

        # add information
        sender = message.get_sender()
        text = translate("email app", "From: {sender}").format(sender=sender)
        paragraphs.insert(0, text)

        subject = message.get_subject()
        text = translate("email app", "Subject: {subject}").format(subject=subject)
        paragraphs.insert(1, text)

        text = translate("email app", "End of email")
        paragraphs.append(text)

        # show paragraphs
        ShowParagraphedText(
                              self._view,
                              paragraphs,
                              lambda index: self._global_config.say(paragraphs[index]),
                              lambda index: self._global_config.say(paragraphs[index]),
                              back
                            )()
