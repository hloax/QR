import tkinter as tk
from tkinter import messagebox
from qr_scanner import QRScanner
from exporter import export_to_excel

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="QR Attendance Register", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self, text="Check-In", command=lambda: master.switch_page(QRScanner, 'check_in')).pack(pady=10)
        tk.Button(self, text="Check-Out", command=lambda: master.switch_page(QRScanner, 'check_out')).pack(pady=10)
        tk.Button(self, text="Export Attendance", command=self.export_attendance).pack(pady=10)
        tk.Button(self, text="Clear Data", command=self.clear_data).pack(pady=10)

    def export_attendance(self):
        try:
            attendance_data = self.master.database.get_all_attendance()
            export_to_excel(attendance_data)
            messagebox.showinfo("Success", "Attendance exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_data(self):
        """Clear attendance data and show confirmation dialog."""
        try:
            result = self.master.clear_attendance_data()
            messagebox.showinfo("Success", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))
