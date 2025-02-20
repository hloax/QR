from qr_create import create_qr_code

# Example employee data
name = "Athenkosi"
surname = "Mdashu"
#persal_number = "LEJ054"
department = "Cleaning"

# Generate the QR code
create_qr_code(name, surname, department, output_file="AMdashu.png")
