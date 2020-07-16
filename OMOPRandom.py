import csv
import datetime as dt
import random
import pandas as pd
from faker import Faker

# specify location information for Faker
fake = Faker('en_GB')
fake1 = Faker('en_US')

# CSV file paths
gender_file = 'config_files/gender_id.csv'
race_file = 'config_files/race_id.csv'
ethnicity_file = 'config_files/ethnicity_id.csv'


# creating a random choosing function
def choosing(file):
    df = pd.read_csv(file)
    id_list = df['Id']
    return random.choice(id_list)


# generating all the fields required in PERSON table and filled with random values
class OMOP_PatientRecord:
    person_id = 1
    this_year = dt.datetime.today().year

    # initialize the variables and types
    def __init__(self, records, headers):
        self.records = int(records)
        self.headers = list(headers)

    # generating a random date of birth and time
    def dob_time(self):
        self.sdg_dob = fake1.date_time_ad()
        return self.sdg_dob

    # generating a PERSON table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Person.csv", 'wt') as OMOPcsvFile:
            writer = csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "person_id": OMOP_PatientRecord.person_id,
                    "gender_concept_id": choosing(gender_file),
                    "year_of_birth": self.dob_time().year,
                    "month_of_birth": self.sdg_dob.month,
                    "day_of_birth": self.sdg_dob.day,
                    "birth_datetime": self.sdg_dob,
                    "race_concept_id": choosing(race_file),
                    "ethnicity_concept_id": choosing(ethnicity_file),
                })
                OMOP_PatientRecord.person_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":

    # define the column names for each field according to the OMOP CDM
    header_list = ["person_id", "gender_concept_id", "year_of_birth", "month_of_birth", "day_of_birth",
                   "birth_datetime", "race_concept_id", "ethnicity_concept_id"]

    # the user can customize the number of rows to generate
    while True:
        num_records = input("Please enter the number of OMOP Person records you want to create: ")
        try:
            # checking whether the entered number is valid
            if int(num_records) > 0:
                p1 = OMOP_PatientRecord(num_records, header_list)
                OMOP_PatientRecord.data_generate(p1)
                print("Random OMOP Person CSV generation complete!")
                break
            else:
                print("Please enter a number that is greater than 0.")
        except ValueError:
            print("Please try again and enter a number.")
