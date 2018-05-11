

# Import smtplib for the actual sending function
import smtplib
from os.path import basename, join, exists
from zipfile import ZipFile
from tempfile import gettempdir
from uuid import uuid4

# Import the email modules we'll need
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

emailFrom='techsupport@ese.nyc'
emailTo='tk421storm@gmail.com'

def sendMail(subject, message, attachments=None, zipAttachments=True):
	'''send an email to the archivist list'''
	
	message=message.replace("\n", "<br />")
	
	# Create a text/plain message
	msg = MIMEMultipart()
	
	# me == the sender's email address
	# you == the recipient's email address
	msg['Subject'] = subject
	msg['From'] = emailFrom
	msg['To'] = emailTo
	msg['Date'] = formatdate(localtime=True)
	
	msg.attach(MIMEText(message, 'html'))
	
	#zip the attachment
	if zipAttachments and attachments:
		zipFile=join(gettempdir(), uuid4().hex+'.emailAttachments.zip')
		for filePath in attachments:
			if exists(filePath):
				fileName=basename(filePath)

				with ZipFile(zipFile, 'a') as myZip:
					myZip.write(filePath, fileName)
				
		with open(zipFile, "rb") as fil:
			part = MIMEApplication(
	            fil.read(),
	            Name=basename(zipFile)
	        )
		# After the file is closed
		part['Content-Disposition'] = 'attachment; filename="%s"' % basename(zipFile)
		msg.attach(part)
	elif attachments and not zipAttachments:
		raise IOError('emailing non-zipped attachments is currently not supported')
	
	msg.add_header('Content-Type', 'text/html')

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP_SSL('a2plcpnl0220.prod.iad2.secureserver.net')
	s.login('techsupport@ese.nyc', '3astsid3')
	s.sendmail(emailFrom, [emailTo], msg.as_string())
	s.quit()