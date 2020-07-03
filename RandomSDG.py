import csv
from faker import Faker
import datetime as dt


def datagenerate(records, headers):
    this_year = dt.datetime.today().year
    fake = Faker('en_GB')
    fake1 = Faker('en_US')
    user_id = 1

    with open("Patient_data.csv", 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()

        for i in range(records):
            sdg_dob = fake1.date_time_ad()
            writer.writerow({
                "PERSON_ID": user_id,
                "Patient Name": fake.name(),
                "BIRTH_DATETIME": sdg_dob,
                "Age": this_year - sdg_dob.year,
                "Phone Number": fake.phone_number(),
                "Address": fake.address(),
                "Zip Code": fake.postcode(),
                "City": fake.city(),
            })
            user_id += 1


records = 10000
headers = ["PERSON_ID", "Patient Name", "BIRTH_DATETIME", "Age",
           "Phone Number", "Address", "Zip Code", "City"]
datagenerate(records, headers)
print("CSV generation complete!")
