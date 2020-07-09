import csv
import datetime as dt
import random
from faker import Faker

fake = Faker('en_GB')
fake1 = Faker('en_US')


def gender_id():
    # Male: 8507, Female: 8532
    return random.choice([8507, 8532])


def race_id():
    race_id_list = [38003572, 38003573, 38003574, 38003575, 38003576, 38003577, 38003578, 38003579, 38003580, 38003581,
                    38003582, 38003583, 38003584, 38003585, 38003586, 38003587, 38003588, 38003589, 38003590, 38003591,
                    38003592, 38003593, 38003594, 38003595, 38003596, 38003597, 38003598, 38003599, 38003600, 38003601,
                    38003602, 38003603, 38003604,38003605, 38003606, 38003607, 38003608, 38003609, 38003610, 38003611,
                    38003612, 38003613, 38003614, 38003615,38003616, 8515, 8516, 8527, 8557, 8657]
    return random.choice(race_id_list)


def ethnicity_id():
    # Hispanic or Latino: 38003563, Not Hispanic or Latino: 38003564
    return random.choice([38003563, 38003564])


class OMOP_PatientRecord:
    person_id = 1
    this_year = dt.datetime.today().year

    def __init__(self, records, headers):
        self.records = int(records)
        self.headers = list(headers)

    def dob_time(self):
        self.sdg_dob = fake1.date_time_ad()
        return self.sdg_dob

    def data_generate(self):
        with open("Random_OMOP_Person.csv", 'wt') as OMOPcsvFile:
            writer = csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "person_id": OMOP_PatientRecord.person_id,
                    "gender_concept_id": gender_id(),
                    "year_of_birth": self.dob_time().year,
                    "month_of_birth": self.sdg_dob.month,
                    "day_of_birth": self.sdg_dob.day,
                    "birth_datetime": self.sdg_dob,
                    "race_concept_id": race_id(),
                    "ethnicity_concept_id": ethnicity_id(),
                })
                OMOP_PatientRecord.person_id += 1
            OMOPcsvFile.close()


header_list = ["person_id", "gender_concept_id", "year_of_birth", "month_of_birth", "day_of_birth", "birth_datetime",
               "race_concept_id", "ethnicity_concept_id"]


if __name__ == "__main__":
    while True:
        num_records = input("Please enter the number of OMOP Person records you want to create: ")
        try:
            if int(num_records) > 0:
                p1 = OMOP_PatientRecord(num_records, header_list)
                OMOP_PatientRecord.data_generate(p1)
                print("Random OMOP Person CSV generation complete!")
                break
            else:
                print("Please enter a number that is greater than 0.")
        except ValueError:
            print("Please try again and enter a number.")
