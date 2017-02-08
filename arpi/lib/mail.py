import os
import time
import datetime
import email
import imaplib

import imaplib



class Account:
    def __init__(self, host, username, password):
        self.server = imaplib.IMAP4_SSL(host)
        self.server.login(username, password)
        self.server.select("INBOX")
    
    def get_messages(self,n):
        result, data = self.server.search(None, "ALL")
        if result != 'OK':
            raise RuntimeError("IMAP failed")

        email_ids = data[0].split()
        
        messages = []
        
        for email_id in email_ids[-n:]:
            # (RFC822) = email body
            result, data = self.server.fetch(email_id, "(RFC822)")
            
            if result != 'OK':
                raise RuntimeError("IMAP failed")
            
            messages.append( Message(data[0][1]) )
        
        return messages

class Message:
    def __init__(self, msg):
        self._msg = email.message_from_bytes(msg)
    
    def get_sender(self):
        """
        Get the message's sender
        """
        sender = self._msg['From']
        realname, emailaddress = email.utils.parseaddr(sender)
        if realname:
            return realname.strip()
        elif emailaddress:
            accountname = emailaddress.split('@')[0]
            return accountname.replace('.',' ').replace('-',' ').replace('_',' ').strip()
        else:
            return "Unknown"
    
    def get_subject(self):
        """
        Get the message's subject
        """
        return self._msg['Subject'].strip()
    
    def get_datetime(self):
        """
        Get the message's date time
        """
        date = self._msg['Date']
        date_tuple = email.utils.parsedate(date)
        timestamp = time.mktime(date_tuple)
        return datetime.datetime.fromtimestamp(timestamp)
    
    def get_text(self):
        """
        Get the message text. Distinguish multipart and non-multipart messages.
        """
        # based on: http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
        if self._msg.is_multipart():
            for part in self._msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    content_charsets = part.get_charsets()
                    content_charset = content_charsets[0] if content_charsets else "UTF-8"
                    return str( part.get_payload(decode=True), content_charset, "replace" )
        else:
            content_charsets = self._msg.get_charsets()
            content_charset = content_charsets[0] if content_charsets else "UTF-8"
            return str( self._msg.get_payload(decode=True), content_charset, "replace" )
