import csv
from faker import Faker
import datetime as dt

fake = Faker('en_GB')
fake1 = Faker('en_US')

'''generating random data for patient record'''


def person_id():
    return PatientRecord.user_id


def person_name():
    return fake.name()


def phone_num():
    return fake.phone_number()


def address():
    return fake.street_address()


def city():
    return fake.city()


def p_code():
    return fake.postcode()


class PatientRecord:
    user_id = 1
    this_year = dt.datetime.today().year

    def __init__(self, records, headers):
        self.records = int(records)
        self.headers = list(headers)

    def dob_time(self):
        self.sdg_dob = fake1.date_time_ad()
        return self.sdg_dob

    def age(self):
        return PatientRecord.this_year - self.sdg_dob.year

    def data_generate(self):
        with open("Patient_data.csv", 'wt') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "PERSON_ID": person_id(),
                    "Patient Name": person_name(),
                    "BIRTH_DATETIME": self.dob_time(),
                    "Age": self.age(),
                    "Phone Number": phone_num(),
                    "Address": address(),
                    "City": city(),
                    "Zip Code": p_code()
                })
                PatientRecord.user_id += 1


header_list = ["PERSON_ID", "Patient Name", "BIRTH_DATETIME", "Age",
               "Phone Number", "Address", "Zip Code", "City"]
while True:
    num_records = input("Please enter the number of patient records you want to create: ")
    try:
        if int(num_records) > 0:
            p1 = PatientRecord(num_records, header_list)
            PatientRecord.data_generate(p1)
            print("CSV generation complete!")
            break
        else:
            print("Please enter a number that is greater than 0.")
    except ValueError:
        print("Please try again and enter a number.")
