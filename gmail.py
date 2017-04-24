#!/usr/bin/env python
#coding: utf-8
 
import imaplib
import email
import time
import Settings

def check():
    ret = []
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(LOGIN_USER, LOGIN_PASS)
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
            if text[0:len(REMOTE_SUBJECT)] == REMOTE_SUBJECT:
                # Get Body
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        lines = part.get_payload().splitlines()
                        ret.append(lines)
                        break
    mail.logout()
    return ret
