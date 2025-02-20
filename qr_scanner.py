import cv2
import json
from pyzbar.pyzbar import decode
from tkinter import Frame
import tkinter.messagebox as messagebox

class QRScanner(Frame):
    def __init__(self, master, action):
        super().__init__(master)
        self.master = master
        self.action = action
        self.database = master.database

    def start_scanner(self):
        """
        Starts the camera to scan QR codes.
        """
        cap = cv2.VideoCapture(0)  # Open the default camera (0)
        scanned = False

        while not scanned:
            ret, frame = cap.read()  # Capture each frame
            if not ret:
                print("Failed to open camera. Exiting.")
                break

            # Decode QR codes in the frame
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print("QR Data:", qr_data)  # For debugging
                scanned = True
                self.process_qr_code(qr_data)
                break

            # Display the frame with OpenCV
            cv2.imshow("QR Code Scanner", frame)

            # Close the scanner if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_qr_code(self, qr_data):
        """
        Process the scanned QR code data.
        """
        try:
            # Parse the JSON data from the QR code
            employee_data = json.loads(qr_data)

            #Error handling
            required_keys = ["name", "surname", "persal_number", "department"]
            for key in required_keys:
                if key not in employee_data:
                    raise ValueError(f"Missing required key: {key}")

            #Extract details
            name = employee_data["name"]
            surname = employee_data["surname"]
            persal_number = employee_data["persal_number"]
            department = employee_data["department"]

            # Check-in or check-out based on the action
            if self.action == "check_in":
                message = self.database.check_in(name, surname, persal_number, department)
            elif self.action == "check_out":
                message = self.database.check_out(persal_number)
            else:
                message = "Unknown action."

            # Display a confirmation message
            messagebox.showinfo("QR Attendance", message)
        
        except json.JSONDecodeError:
            messagebox.showerror("QR Attendance", "Invalid QR code data.")
