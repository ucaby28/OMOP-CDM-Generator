import random
import pandas as pd
import Random as rd

# CSV file paths for pre-stored IDs
gender_file = 'config_files/gender_id.csv'
race_file = 'config_files/race_id.csv'
ethnicity_file = 'config_files/ethnicity_id.csv'

# define the column names for each field according to the OMOP CDM
header_list = ["person_id", "gender_concept_id", "year_of_birth", "month_of_birth", "day_of_birth",
               "birth_datetime", "race_concept_id", "ethnicity_concept_id"]

# messages to display at CLI
m1 = "Please enter the number of OMOP Person records you want to create: "
m2 = "Random OMOP Person CSV generation complete!"


# creating a random choosing function
def choosing(file):
    df = pd.read_csv(file)
    id_list = df['Id']
    return random.choice(id_list)


# obtaining user input and generating data
def main(msg1, msg2, header):
    # the user can customize the number of rows to generate
    while True:
        num_records = input(msg1)
        try:
            # checking whether the entered number is valid
            if int(num_records) > 0:
                OMOP_PatientRecord(num_records, header).data_generate()
                print(msg2)
                break
            else:
                print("Please enter a number that is greater than 0.")
        except ValueError:
            print("Please try again and enter a number.")


# generating all the fields required in PERSON table and filled with random values
class OMOP_PatientRecord(rd.PatientRecord):

    # generating a PERSON table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Person.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
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
    main(m1, m2, header_list)
