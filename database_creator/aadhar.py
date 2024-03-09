import random
import csv
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
fake = Faker('en_IN')  # Set locale to Indian English
number_of_entries = 200
x = input("\n\nARE YOU REALLY WANNA DO THIS\n\n")
if x!= "password":
    exit()
def random_date_of_birth(start_date=datetime(1950, 1, 1), end_date=datetime(2000, 12, 31)):
    """
    Generates a random date of birth between start_date and end_date.
    """
    if not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    if not isinstance(end_date, datetime):
        end_date = datetime.combine(end_date, datetime.min.time())

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def generate_unique_adhar_number(existing_adhar_numbers):
    """
    Generates a unique Aadhar number that is not in the set existing_adhar_numbers.
    """
    adhar_number = None
    while adhar_number is None or adhar_number in existing_adhar_numbers:
        adhar_number = int("%0.12d" % random.randint(10**11, 10**12 - 1))
    return adhar_number

def generate_unique_phone_number(existing_phone_numbers):
    """
    Generates a unique phone number that is not in the set existing_phone_numbers.
    """
    phone_number = None
    while phone_number is None or phone_number in existing_phone_numbers:
        phone_number = random_phone_number()
    return phone_number

def generate_unique_name(existing_names, gender):
    """
    Generates a unique name that is not in the set existing_names.
    """
    name = None
    while name is None or name in existing_names:
        name = fake.first_name_male() if gender == "M" else fake.first_name_female()
    return name

def random_phone_number():
    """
    Generates a random phone number in India format.
    """
    # Generate random digits for the phone number
    phone_digits = [random.randint(0, 9) for _ in range(10)]

    # Ensure the first digit is between 6 and 9 to comply with Indian phone number rules
    phone_digits[0] = random.randint(6, 9)

    # Format the phone number
    phone_number = ''.join(map(str, phone_digits))
    formatted_phone_number = f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"

    return formatted_phone_number

class Adhar:
    def __init__(self, adharnumber=None, first_name=None, last_name=None, date_of_birth=None, gender=None, phno=None, district=None):
        self.adharnumber = adharnumber
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phno = phno
        self.district = district

DATABASE = []
existing_adhar_numbers = set()
existing_phone_numbers = set()
existing_names = set()

kerala_districts = ["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]

while number_of_entries:
    # Generate a random gender
    gender = random.choice(["M", "F"])

    # Generate unique Aadhar number, phone number, and name
    adhar_number = generate_unique_adhar_number(existing_adhar_numbers)
    phone_number = generate_unique_phone_number(existing_phone_numbers)
    name = generate_unique_name(existing_names, gender)

    last_name = fake.last_name()

    entry = Adhar(
        adharnumber=adhar_number,
        first_name=name,
        last_name=last_name,
        date_of_birth=random_date_of_birth(),
        gender=gender,
        phno=phone_number,
        district=random.choice(kerala_districts)
    )
    DATABASE.append(entry)

    # Add generated values to sets
    existing_adhar_numbers.add(adhar_number)
    existing_phone_numbers.add(phone_number)
    existing_names.add(name)

    number_of_entries -= 1

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Adhar Number', 'First Name', 'Last Name', 'Date of Birth', 'Gender', 'Phone Number', 'District']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            writer.writerow({'Adhar Number': entry.adharnumber,
                             'First Name': entry.first_name,
                             'Last Name': entry.last_name,
                             'Date of Birth': entry.date_of_birth,
                             'Gender': entry.gender,
                             'Phone Number': entry.phno,
                             'District': entry.district})

write_to_csv(DATABASE, 'adhar_database.csv')
df = pd.read_csv('adhar_database.csv')
print(df)
