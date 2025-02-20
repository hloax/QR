import qrcode
import json

def create_qr_code(name, surname, department, output_file="qr_code.png"):
    """
    Generates a QR code with structured data for an employee.

    Args:
        name (str): Employee's first name.
        surname (str): Employee's surname.
        persal_number (str): Employee's unique identifier.
        department (str): Employee's department.
        output_file (str): File name for the generated QR code.
    """
    # Create structured data as a JSON string
    qr_data = {
        "name": name,
        "surname": surname,
        #"persal_number": persal_number,
        "department": department
    }
    qr_data_json = json.dumps(qr_data)

    # Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data_json)
    qr.make(fit=True)

    # Save the QR code to an image file
    img = qr.make_image(fill="black", back_color="white")
    img.save(output_file)

    print(f"QR code saved to {output_file}.")
