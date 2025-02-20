import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("attendance.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                persal_number TEXT,
                department TEXT,
                check_in_date TEXT,
                check_in_time TEXT,
                check_out_date TEXT,
                check_out_time TEXT,
                total_hours REAL
            )
        ''')
        self.connection.commit()

    def check_in(self, name, surname, persal_number, department):
        # Check if already checked in today
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            '''
            SELECT * FROM attendance 
            WHERE persal_number = ? AND check_in_date = ? AND check_out_time IS NULL
            ''', 
            (persal_number, today)
        )
        if self.cursor.fetchone():
            return f"User {name} {surname} has already checked in today."

        # Insert a new record
        check_in_date = datetime.now().strftime("%Y-%m-%d")
        check_in_time = datetime.now().strftime("%H:%M:%S")
        self.cursor.execute(
            '''
            INSERT INTO attendance (name, surname, persal_number, department, check_in_date, check_in_time) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (name, surname, persal_number, department, check_in_date, check_in_time)
        )
        self.connection.commit()
        return f"Check-in successful for {name} {surname}."


    def check_out(self, persal_number):
        # Check if there is an active check-in record
        self.cursor.execute(
            '''
            SELECT id, check_in_date, check_in_time FROM attendance 
            WHERE persal_number = ? AND check_out_time IS NULL
            ''', 
            (persal_number,)
        )
        record = self.cursor.fetchone()
        if not record:
            return "No active check-in record found."

        # Update the check-out time and calculate total hours
        check_out_date = datetime.now().strftime("%Y-%m-%d")
        check_out_time = datetime.now().strftime("%H:%M:%S")
        check_in_time = datetime.strptime(f"{record[1]} {record[2]}", "%Y-%m-%d %H:%M:%S")
        total_hours = (datetime.now() - check_in_time).total_seconds() / 3600

        self.cursor.execute(
            '''
            UPDATE attendance 
            SET check_out_date = ?, check_out_time = ?, total_hours = ? 
            WHERE id = ?
            ''', 
            (check_out_date, check_out_time, total_hours, record[0])
        )
        self.connection.commit()
        return f"Check-out successful. Total hours worked: {total_hours:.2f}."


    def get_all_attendance(self):
        self.cursor.execute(
            '''
            SELECT id, name, surname, persal_number, department,
              check_in_date, check_in_time, check_out_date, check_out_time, total_hours
            FROM attendance
            '''
        )
        rows = self.cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "persal_number": row[3],
                "department": row[4],
                "check_in_date": row[5],
                "check_in_time": row[6],
                "check_out_date": row[7],
                "check_out_time": row[8],
                "total_hours": row[9]
            }
            for row in rows
        ]
    
    def clear_all_attendance(self):
        """Delete all attendance records from the database."""
        self.cursor.execute('DELETE FROM attendance')
        self.connection.commit()
        return "All attendance records have been cleared."

    def close(self):
        self.connection.close()
