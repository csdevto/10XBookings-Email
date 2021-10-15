import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    BookingSQL = "CREATE TABLE IF NOT EXISTS `Bookings` ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT , `EmailID` TEXT NOT NULL , `StartTime` DATETIME NOT NULL , `Status` TEXT NOT NULL , `Description` TEXT NOT NULL);"
    AdminSQL = "CREATE TABLE IF NOT EXISTS `Admin` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT , `Key` TEXT NOT NULL, `Value` INTEGER NOT NULL)"
    conn = create_connection('/DB/bookings.db')
    create_table(conn,BookingSQL)
    create_table(conn,AdminSQL)
