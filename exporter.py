import pandas as pd

def export_to_excel(attendance_data, file_name="attendance_register.xlsx"):
    # Validate the format of attendance_data
    if not isinstance(attendance_data, list) or not all(isinstance(record, dict) for record in attendance_data):
        raise ValueError("Invalid attendance data format. Expected a list of dictionaries.")

    # Create a DataFrame
    try:
        df = pd.DataFrame(attendance_data)
        df.to_excel(file_name, index=False)
        print(f"Attendance register exported to {file_name}.")
    except Exception as e:
        print(f"Failed to export attendance: {e}")
