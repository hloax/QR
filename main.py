import tkinter as tk
from qr_attendance_gui import MainMenu
from qr_scanner import QRScanner
from database import Database
from exporter import export_to_excel

class QRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Attendance Register")
        self.geometry("400x300")

        # Initialize Database
        self.database = Database()

        # Show the main menu
        self.current_page = MainMenu(self)
        self.current_page.pack()

    def switch_page(self, page_class, *args):
        self.current_page.pack_forget()
        self.current_page.destroy()
        if page_class == QRScanner:
            scanner = QRScanner(self, *args)
            scanner.start_scanner()  # Directly start the scanner
            # Return to MainMenu after scanning
            self.current_page = MainMenu(self)
        else:
            self.current_page = page_class(self, *args)
        self.current_page.pack()

    def export_attendance_data(self):
        """Export attendance data to an excel file."""
        attendance_data = self.database.get_all_attendance()
        export_to_excel(attendance_data)
        print("Attendance data exported successfully!")

    def clear_attendance_data(self):
        """Clear all attendance data from the database."""
        return self.database.clear_all_attendance()
        #print(result)
        #return result
    
def main():
    #Test export functionality
    database = Database()
    attendance_data = database.get_all_attendance()
    export_to_excel(attendance_data)
    print ("Attendance export test completed")

    # Launch application
    app = QRApp()
    app.mainloop()

if __name__ == "__main__":
    main()
