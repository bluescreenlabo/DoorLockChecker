#!/usr/bin/env python
#coding: utf-8
 
import imaplib
import email
import time
import Settings

def check():
    lines = []
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(Settings.LOGIN_USER, Settings.LOGIN_PASS)
    mail.list()
    mail.select('inbox')
    # New Mail?
    stat, mlist = mail.search(None, '(UNSEEN)')
    if mlist[0] is not '':
        for num in mlist[0].split():
            res, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_string(data[0][1])
            # Get Subject
            subject = email.Header.decode_header(msg.get('Subject'))
            text, charset = subject[0]
            if text[0:len(Settings.REMOTE_SUBJECT)] == Settings.REMOTE_SUBJECT:
                # Get Body
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        lines = part.get_payload().splitlines()
                        while (True):
                            try:
                                lines.remove("")
                            except:
                                break
                        break
    mail.logout()
    return lines

if __name__ == '__main__':
    try:
        check()
    except KeyboardInterrupt:
        pass
