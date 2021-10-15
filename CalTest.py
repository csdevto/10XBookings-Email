from datetime import datetime
import caldav
from dotenv import load_dotenv
import os 

#Config for Caldav
CalEmail = os.environ.get('CalEmail')#if using same mail client use email and password from above
CalPassword = os.environ.get('CalPassword') #same as above if same account
CalDavURL=['https://caldav.icloud.com','https://www.google.com/calendar/dav/' + CalEmail + '/user']
caldav_url = CalDavURL[0] #pick between 0 Icloud and 1 Google
CalendarName = 'Test' #Calendar Name

#Start Caldav
client = caldav.DAVClient(url=caldav_url, username=CalEmail, password=CalPassword)
my_principal = client.principal()
my_new_calendar=''

## The principals calendars can be fetched like this:
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

my_new_calendar = my_principal.calendar(name="Test")
assert(my_new_calendar)

start = datetime(2021, 10, 9)
end = datetime(2021, 10, 10)
print(end)
events_fetched = my_new_calendar.date_search(start=start, end=end, expand=True)
print(f"t: {events_fetched}")
for x in events_fetched:
    if x.data.find("10X:") != -1:
        #x.delete()
        print(x.data)
