#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
import imaplib
import smtplib

class GmailClient(object):
	def __init__(self, user, password):
		self.user = user
		self.password = password
		self.smtp_host = 'smtp.gmail.com'
		self.smtp_port = 465
		self.imap_host = 'imap.gmail.com'
		self.imap_port = 993
		self.email_default_encoding = 'iso-2022-jp'

	def sendMail(self, from_address, to_addresses, cc_addresses, bcc_addresses, subject, body):
		"""
		Args:
			to_addresses: must be a list
			cc_addresses: must be a list
			bcc_addresses: must be a list
		"""
		mail = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
		mail.login(self.user, self.password)
		msg = MIMEText(body, 'plain', self.email_default_encoding)
		msg['Subject'] = Header(subject)
		msg['From'] = from_address
		msg['To'] = ', '.join(to_addresses)
		if cc_addresses:
			msg['CC'] = ', '.join(cc_addresses)
		if bcc_addresses:
			msg['BCC'] = ', '.join(bcc_addresses)
		mail.sendmail(from_address, to_addresses, msg.as_string())
		mail.close()
		mail.logout()

	def getMail(self):
		ret = {
			'from_address': '',
			'to_addresses': '',
			'cc_addresses': '',
			'bcc_addresses': '',
			'date': '',
			'subject': '',
			'body': [],
		}
		mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
		mail.login(self.user, self.password)
		mail.list()
		mail.select('inbox')
		stat, mlist = mail.search(None, '(UNSEEN)')
		if mlist[0] is not '':
			for num in mlist[0].split():
				res, data = mail.fetch(num, '(RFC822)')
				msg = email.message_from_string(data[0][1])
				
				subject, charset = email.Header.decode_header(msg.get('Subject'))[0]
				for part in msg.walk():
					if part.get_content_type() == 'text/plain':
						lines = part.get_payload().splitlines()
						break
				ret = {
					'from_address': msg.get('From'),
					'to_addresses': msg.get('To'),
					'cc_addresses': msg.get('CC'),
					'bcc_addresses': msg.get('BCC'),
					'date': msg.get('Date'),
					'subject': subject,
					'body': lines,
				}
		mail.close()
		mail.logout()
		return ret

if __name__ == '__main__':
	email_address = raw_input("Enter email address: ")
	email_password = raw_input("Enter email password: ")
	
	Gmail = GmailClient(email_address, email_password)
	
	# Send an email to myself
	Gmail.sendMail(email_address, [email_address], None, None, u"テスト", u"テストメールです")

	# Check the email
	email = Gmail.getEmail()
	print "from_address=%s" % email['from_address']
	print "to_addresses=%s" % email['to_addresses']
	print "cc_addresses=%s" % email['cc_addresses']
	print "bcc_addresses=%s" % email['bcc_addresses']
	print "date=%s" % email['date']
	print "subject=%s" % email['subject']
	print "body=%s" % email['body']

