from PIL import Image
import datetime
import os
from pdf417gen import encode, render_image
from Code128 import Code128Encoder  # Import Code128Encoder from Code128 library

def get_user_input():
    license_number = input("Enter License Number: ")
    issue_date = input("Enter Issue Date (MMDDYYYY): ")

    # Calculate expiration date
    issue_date_obj = datetime.datetime.strptime(issue_date, "%m%d%Y")
    expiry_date_obj = issue_date_obj + datetime.timedelta(days=365 * 5)  # Assuming a 5-year expiration
    expiry_date = expiry_date_obj.strftime("%m%d%Y")

    dob = input("Enter Date of Birth (MMDDYYYY): ")
    name = input("Enter Full Name: ")
    address = input("Enter Address: ")

    sex_options = ["M", "F"]
    sex = input("Enter Sex (M/F): ").upper()
    while sex not in sex_options:
        print("Invalid input. Please enter M or F.")
        sex = input("Enter Sex (M/F): ").upper()

    height = input("Enter Height (e.g., 5-10): ")
    weight = input("Enter Weight in lbs: ")

    # Eye color options
    eye_color_options = ["BLU", "BRO", "GRN", "HAZ", "GRY"]
    print("Eye Color Options:", eye_color_options)
    eye_color = input("Enter Eye Color: ").upper()
    while eye_color not in eye_color_options:
        print("Invalid input. Please choose from the provided options.")
        eye_color = input("Enter Eye Color: ").upper()

    # Hair color options
    hair_color_options = ["BLK", "BRO", "BLN", "RED", "SDY", "GRY", "WHI", "UNK"]
    print("Hair Color Options:", hair_color_options)
    hair_color = input("Enter Hair Color: ").upper()
    while hair_color not in hair_color_options:
        print("Invalid input. Please choose from the provided options.")
        hair_color = input("Enter Hair Color: ").upper()

    license_class = input("Enter License Class: ")

    # Endorsements
    endorsements_input = input("Do you have endorsements? (yes/no): ").lower()
    endorsements = input("Enter Endorsements: ") if endorsements_input == 'yes' else "NONE"

    # Restrictions
    restrictions_input = input("Do you have restrictions? (yes/no): ").lower()
    restrictions = input("Enter Restrictions: ") if restrictions_input == 'yes' else "NONE"

    # Automatically calculate DD Info
    dd_info = f"054H{license_number}NENOCO0123146"  # Modify this based on your calculation logic

    return (
        license_number, issue_date, expiry_date, dob, name, address,
        sex, height, weight, license_class, endorsements, restrictions,
        eye_color, hair_color, dd_info
    )

def generate_barcodes(license_number, issue_date, expiry_date, dob, name, address, sex, height, weight, license_class, endorsements, restrictions, eye_color, hair_color, dd_info):
    # Create a folder for each user based on their full name
    folder_name = name.replace(' ', '_')
    os.makedirs(folder_name, exist_ok=True)

    # Generate PDF417 barcode
    data_to_encode_pdf417 = f"@ANSI636054100002DL00410280ZN03210038DLDAQH{license_number}DCS{name.replace(' ', '')}DDEN DAC{name.replace(' ', '')}DDFN DADA DDGN DCAO DCBB DCDNONE DBD{issue_date}DBB{dob}DBA{expiry_date}DBC1DAU{sex}inDAY{height}DAG{address}DAJNEDAK{weight}DCF{dd_info}DDAFDDGN DCAO DCBB DCDNONE"
    pdf417 = encode(data_to_encode_pdf417)
    pdf417_image = render_image(pdf417, scale=3, padding=10)
    pdf417_image.save(f'{folder_name}/generated_barcode_pdf417.png')

    # Generate CODE_128 barcode using Code128 library
    data_to_encode_code128 = f"{license_number}{dob}{issue_date}{expiry_date}"
    code128_encoder = Code128Encoder(data_to_encode_code128, options={'ttf': True})
    code128_image = code128_encoder.save(f'{folder_name}/generated_barcode_code128.png')

# Get user input
user_input = get_user_input()

# Generate barcodes using user input
generate_barcodes(*user_input)
