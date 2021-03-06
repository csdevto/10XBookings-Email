"""

"""
import email
import imaplib
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import time
import re
import json
from dotenv import load_dotenv
import os 
#For Calendars
import caldav

load_dotenv()
#Config Mail
SERVER=os.environ.get('IMAPServer') #imapserver address
MailEmail= os.environ.get('MailEmail') #your email address
MailPassword=os.environ.get('MailPassword') #app specific passowrd (prevents two factor authenticator)
EmailFolder = os.environ.get('EmailFolder')#folder hoding emails for bookings - create a rule to move booking confirmations

#Initiate email Imap
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(MailEmail, MailPassword)

#Config for Caldav
CalEmail = os.environ.get('CalEmail')#if using same mail client use email and password from above
CalPassword = os.environ.get('CalPassword') #same as above if same account
CalDavURL=['https://caldav.icloud.com','https://www.google.com/calendar/dav/' + CalEmail + '/user']
Cal = int(os.environ.get('CalendarService'))
caldav_url = CalDavURL[Cal] #pick between 0 Icloud and 1 Google
CalendarName = os.environ.get('CalendarName') #Calendar Name

#Start Caldav
client = caldav.DAVClient(url=caldav_url, username=CalEmail, password=CalPassword)
my_principal = client.principal()
my_new_calendar=''


#regex to extract date, time and court number
DateRegex = re.compile(
    "(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|"
    "Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|"
    "Dec(ember)?)\s+\d{1,2},\s+\d{4}")
TimeRegex = re.compile("\d{1,2}:\d{2} (:?AM|PM|am|pm)")

def GetCalendarList():
    calendars = my_principal.calendars()
    if calendars:
    ## Some calendar servers will include all calendars you have
    ## access to in this list, and not only the calendars owned by
    ## this principal.
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("    Name: %-20s  URL: %s" % (c.name, c.url))
        else:
            print("your principal has no calendars")
def CreateCalendar(CalName,DTSTART,DTEND,Summary):
    ## Let's try to find or create a calendar ... ##f FOR GOOGLE NEED TO CHECK WHY IT CANT CREATE CALENDAR

    my_new_calendar =''
    try:
        ## This will raise a NotFoundError if calendar does not exist
        my_new_calendar = my_principal.calendar(name=CalName)
        assert(my_new_calendar)
        ## calendar did exist, probably it was made on an earlier run
        ## of this script
    except caldav.error.NotFoundError:
        ## Let's create a calendar
        my_new_calendar = my_principal.make_calendar(name=CalName)

    my_new_calendar.save_event(f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID: {DTSTART + DTEND + Summary}
DTSTART:{DTSTART}
DTEND:{DTEND}
SUMMARY:{Summary}
END:VEVENT
END:VCALENDAR
""")

def MailBoxes():
    for i in mail.list()[1]:
        l = i.decode().split(' "/" ')
        print(l[1])

def writelist(List,FileName):
    try:
        with open('DB/' + FileName + '.txt','w') as filehandle:
            json.dump(List, filehandle)
    except FileNotFoundError:
        os.mkdir('DB')
        with open('DB/' + FileName + '.txt','w') as filehandle:
            json.dump(List, filehandle)
def readlist(FileName):
    try:
        with open('DB/' + FileName + '.txt', 'r') as filehandle:
            return json.load(filehandle)
    except FileNotFoundError:
        a = []
        return a

def BookingConfirmation():
    mail.select(EmailFolder)
    OldID = readlist('Confirmation')
    status, data = mail.search(None, '(FROM "Info@TenXToronto.com" SUBJECT "10XTO: Schedule Confirmation")')
    mail_ids = []
    for block in data:
        mail_ids += block.split()
    for i in mail_ids[-20:]:
        id = (f"{i}")
        if id not in OldID:
            OldID.append(id)
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
                    soup = BeautifulSoup(''.join(mail_content),"lxml")
                    soup = soup.findAll('strong')[0].next
                    
                    BDate = DateRegex.search(soup).group()
                    BTime = TimeRegex.search(soup).group()
                    BookingTime = datetime.strptime(BDate + " " + BTime,"%B %d, %Y %I:%M %p")
                    EndTime = BookingTime + timedelta(hours=1)
                    BookingTime = BookingTime.strftime('%Y%m%dT%H%M%S')
                    EndTime = EndTime.strftime('%Y%m%dT%H%M%S')
                    try:
                        location = (soup.split("on",1)[1]).replace("=\r\n", "")
                    except:
                        location = "Booking Confirmation"
                    BLocation = "10X:" + location
                    CreateCalendar(CalendarName,BookingTime,EndTime,BLocation)
    print(OldID)
    writelist(OldID,'Confirmation')
#print(GetCalendarList())
def DeleteBooking():
    mail.select(EmailFolder)
    OldID = readlist('Cancellation')
    status, data = mail.search(None, '(FROM "Info@TenXToronto.com" SUBJECT "10XTO: Schedule Cancellation")')
    mail_ids = []
    for block in data:
        mail_ids += block.split()
    for i in mail_ids[-10:]:
        id = (f"{i}")
        if id not in OldID:
            OldID.append(id)
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
                    soup = BeautifulSoup(''.join(mail_content),"lxml")
                    soup = soup.findAll('strong')[0].next
                    
                    BDate = DateRegex.search(soup).group()
                    BTime = TimeRegex.search(soup).group()
                    Start = datetime.strptime(BDate,"%B %d, %Y")
                    Start = Start
                    EndDate = Start + timedelta(days=1)
                    BookingTime = datetime.strptime(BDate + " " + BTime,"%B %d, %Y %I:%M %p")
                    EndTime = BookingTime + timedelta(hours=1)
                    BookingTime = BookingTime.strftime('%Y%m%dT%H%M%S')
                    EndTime = EndTime.strftime('%Y%m%dT%H%M%S')
                    print(f"{BookingTime} - {EndTime}")
                    try:
                        my_new_calendar = my_principal.calendar(name=CalendarName)
                        assert(my_new_calendar)
                        events_fetched = my_new_calendar.date_search(start=Start, end=EndDate, expand=True)
                        print(f"t: {events_fetched}")
                        for x in events_fetched:
                            if x.data.find("10X:") != -1 and x.data.find(BookingTime) != -1 and x.data.find(EndTime) != -1:
                                print(x.data)
                                x.delete()
                    except AttributeError:
                        print(f"{Start} does not exist")
    print(OldID)
    writelist(OldID,'Cancellation')
    
while True:
    DeleteBooking()
    BookingConfirmation()
    time.sleep(240)
    print('loop')
