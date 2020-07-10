import csv
from faker import Faker
import datetime as dt

fake = Faker('en_GB')
fake1 = Faker('en_US')


# generating a random name
def person_name():
    return fake.name()


# generating a random UK phone number
def phone_num():
    return fake.phone_number()


# generating a random UK address
def address():
    return fake.street_address()


# generating a random UK city
def city():
    return fake.city()


# generating a random UK postcode
def p_code():
    return fake.postcode()


class PatientRecord:
    person_id = 1
    this_year = dt.datetime.today().year

    def __init__(self, records, headers):
        self.records = int(records)
        self.headers = list(headers)

    def dob_time(self):
        self.sdg_dob = fake1.date_time_ad()
        return self.sdg_dob

    def age(self):
        return PatientRecord.this_year - self.sdg_dob.year

    def random_generate(self):
        with open("Random_Patient_Data.csv", 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "PERSON_ID": PatientRecord.person_id,
                    "Patient Name": person_name(),
                    "BIRTH_DATETIME": self.dob_time(),
                    "Age": self.age(),
                    "Phone Number": phone_num(),
                    "Address": address(),
                    "City": city(),
                    "Postcode": p_code()
                })
                PatientRecord.person_id += 1
            csvFile.close()


if __name__ == "__main__":

    # define the column names for each field
    header_list = ["PERSON_ID", "Patient Name", "BIRTH_DATETIME", "Age",
                   "Phone Number", "Address", "City", "Postcode"]

    # the user can customize the number of rows to generate
    while True:
        num_records = input("Please enter the number of patient records you want to create: ")
        try:
            # checking whether the entered number is valid
            if int(num_records) > 0:
                p1 = PatientRecord(num_records, header_list)
                PatientRecord.random_generate(p1)
                print("Random Patient CSV generation complete!")
                break
            else:
                print("Please enter a number that is greater than 0.")
        except ValueError:
            print("Please try again and enter a number.")
