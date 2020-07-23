import csv
from faker import Faker
import datetime as dt

# specify location information for Faker
fake = Faker('en_GB')
fake1 = Faker('en_US')

# messages to display at CLI
m1 = "Please enter the number of patient records you want to create: "
m2 = "Random Patient CSV generation complete!"


# generating a random name
def person_name():
    return fake.name()


# generating a random UK phone number
def phone_num():
    return fake.phone_number()


# obtaining user input and return the input value
def main(msg1, msg2):
    # the user can customize the number of rows to generate
    while True:
        num_records = input(msg1)
        try:
            # checking whether the entered number is valid and return the valid input
            if int(num_records) > 0:
                print(msg2)
                return num_records
            else:
                print("Please enter a number that is greater than 0.")
        except ValueError:
            print("Please try again and enter a number.")


# generating selected fields with random values
class PatientRecord:
    person_id = 1
    this_year = dt.datetime.today().year

    # define the column names for each field
    header_list = ["PERSON_ID", "Patient Name", "BIRTH_DATETIME", "Age",
                   "Phone Number", "Address", "City", "Postcode"]

    # initialize the variables and types
    def __init__(self, records, headers):
        self.records = int(records)
        self.headers = list(headers)

    # generating a random UK address with the corresponding city and postcode
    def address(self):
        self.uk_add = fake.address()
        self.address_list = self.uk_add.split('\n')
        self.postcode = self.address_list[-1]
        self.city = self.address_list[-2]
        return self.uk_add

    # generating a random date of birth and time with the corresponding age
    def dob_time(self):
        self.sdg_dob = fake1.date_time_ad()
        self.age = PatientRecord.this_year - self.sdg_dob.year
        return self.sdg_dob

    # output the random values as a csv file
    def data_generate(self):
        with open("Random_Patient_Data.csv", 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "PERSON_ID": PatientRecord.person_id,
                    "Patient Name": person_name(),
                    "BIRTH_DATETIME": self.dob_time(),
                    "Age": self.age,
                    "Phone Number": phone_num(),
                    "Address": self.address(),
                    "City": self.city,
                    "Postcode": self.postcode
                })
                PatientRecord.person_id += 1
            csvFile.close()


if __name__ == "__main__":
    PatientRecord(main(m1, m2), PatientRecord.header_list).data_generate()
