# 10XBookings-Email
BEFORE RUNNING THE CODE

pip3 install bs4 caldav dotenv

1. MAKE SURE YOU CREATE A FOLDER IN YOUR EMAIL 
   WHERE ALL THE BOOKING CONFIRMATIONS FROM Info@TenXToronto.com
   ARE MOVED FOR PROCESSING
2. MAKE SURE TO CREATE A CALENDAR OR ENTER BELOW AN ALREADY EXCISTING ONE
3. THERE ARE TWO STEPS FOR CONFIGURATION
    1. CREATE A FILE CALLED '.ENV' AND ADD THE FOLLOWING VARIABLES
        IMAPServer=''     #find the IMAP Server for your email account. For google use imap.gmail.com, for outlook use outlook.office365.com
        MailEmail=''      #your email address
        MailPassword=''   #you need to generate an app password to bypass twofactor authenticator. just google it.
        EmailFolder=''    # because of the imap server, the folder should be enclosed in double quotes for example if your folder is called 10XBookings the
                          # line should read EmailFolder='"10XBookings"'
        CalEmail=''       # this is your calendar email, if same as IMAP please use the same credentials
        CalPassword=''    # this is your calendar password, if same as IMAP please use the same credentials or just generate another app password
        CalendarName=''   #Please add your CalendarName where you want to add the booking confirmation
        CalendarService=  #as of right now type 0 for Icloud and 1 for google
        

The code will only look to the 10 newest emails and append a list with the ID
it will run every two minutes and it will check the mailbox for new bookings
once it finds it it will check that the ID doesnt exist in the list and 
it will use CALDAV to create the new calendar.
