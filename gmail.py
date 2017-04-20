#!/usr/bin/env python
#coding: utf-8
 
import imaplib
import email
import time
 
login_user = '*******@gmail.com'
login_pass = '********'
remote_subject = 'RPRemote'
interval = 5

def check():
    ret = []
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(login_user, login_pass)
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
            if text[0:len(remote_subject)] == remote_subject:
                # Get Body
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        lines = part.get_payload().splitlines()
                        ret.append(lines)
                        break
    mail.logout()
    return ret

if __name__ == '__main__':
    try:
        while True:
            ret = check()
            if (ret != []):
                print ret
            time.sleep(interval)
    except KeyboardInterrupt:
        print '\nbreak'
