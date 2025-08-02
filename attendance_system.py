# Import libraries
import sqlite3

# Functions in database
class FunctionsQuery():

    def __init__(self,plate) -> None:
        self.plate = plate

    # Create new database
    def create_database(self):

        connect = sqlite3.connect('/src/database/database.db')
        cursor = connect.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS database(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        names NVARCHAR(50) NOT NULL,
        phone NVARCHAR(11) NOT NULL,
        plate NVARCHAR(8) NOT NULL,
    );
    ''')
        connect.commit()
        connect.close()
        
    # Check registered plate number
    def name_plate(self):
        connect = sqlite3.connect('/src/database/database.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT names FROM database WHERE plate = ?;',(self.plate,))
        connect.commit()
        rows = cursor.fetchall()
        connect.close()
        if rows:
            return rows
        else:
            return 'ثبت نشده'
        
# Create database
if __name__ == '__main__':
    FunctionsQuery('test').create_database()