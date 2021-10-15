import email
import imaplib
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import re
import json
from dotenv import load_dotenv
import os 
#For Calendars
import caldav

#Config Mail
load_dotenv()
#Config Mail
SERVER='imappro.zoho.com' #imapserver address
MailEmail= os.environ.get('MailEmail') #your email address
MailPassword=os.environ.get('MailPassword') #app specific passowrd (prevents two factor authenticator)
EmailFolder = '"/10X/10X Bookings"'
#Initiate email Imap
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(MailEmail, MailPassword)


#regex to extract date, time and court number
DateRegex = re.compile(
    "(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|"
    "Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|"
    "Dec(ember)?)\s+\d{1,2},\s+\d{4}")
TimeRegex = re.compile("\d{1,2}:\d{2} (:?AM|PM|am|pm)")

for i in mail.list()[1]:
    l = i.decode().split(' "/" ')
    #print(l[1])


mail.select(EmailFolder)
status, data = mail.search(None, '(FROM "Info@TenXToronto.com" SUBJECT "10XTO: Schedule Cancellation")')
mail_ids = []
for block in data:
    mail_ids += block.split()
for i in mail_ids[-10:]:
    status, data = mail.fetch(i, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])
            mail_from = message['from']
            mail_subject = message['subject']
            
            if message.is_multipart():
                mail_content = ''
                
                for part in message.get_payload():
                    mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()
            #print(mail_content)
            soup = BeautifulSoup(''.join(mail_content),"lxml")
            soup = soup.findAll('strong')[0].next
            
            BDate = DateRegex.search(soup).group()
            BTime = TimeRegex.search(soup).group()
            BookingTime = datetime.strptime(BDate + " " + BTime,"%B %d, %Y %I:%M %p")
            EndTime = BookingTime + timedelta(hours=1)
            print(f"Start: {BDate} {BTime} End: {EndTime}")