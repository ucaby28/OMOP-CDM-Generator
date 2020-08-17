import OMOPPerson_RD as person
import Random as rd
import pandas as pd
import random

# read CSV files for pre-stored IDs and store them into a list
try:
    person_id_file = 'Random_OMOP_Person.csv'
    person_id_df = pd.read_csv(person_id_file)
    person_id_list = person_id_df['person_id']
except FileNotFoundError:
    person_id_list = [i for i in range(100)]
specimen_concept_file = 'config_files/specimen_concept_id.csv'
specimen_concept_df = pd.read_csv(specimen_concept_file)
specimen_concept_list = specimen_concept_df['Id']
specimen_type_concept_file = 'config_files/specimen_type_concept_id.csv'
specimen_type_concept_df = pd.read_csv(specimen_type_concept_file)
specimen_type_concept_list = specimen_type_concept_df['Id']

# messages to display at CLI
m1 = "Please enter the number of OMOP Specimen records you want to create: "
m2 = "Random OMOP Specimen CSV generation complete!"


# the class that generate random values for all the fields required in Specimen table
class OMOP_PatientRecord(person.OMOP_PatientRecord):
    specimen_id = 1

    # define the column names for each field according to the OMOP CDM
    header_list = ["person_id", "specimen_id", "specimen_concept_id", "specimen_type_concept_id", "specimen_date"]

    # generating a Specimen table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Specimen.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": random.choice(person_id_list),
                    "specimen_id": OMOP_PatientRecord.specimen_id,
                    "specimen_concept_id": random.choice(specimen_concept_list),
                    "specimen_type_concept_id": random.choice(specimen_type_concept_list),
                    "specimen_date": rd.fake1.date_time_ad().date(),
                })
                OMOP_PatientRecord.specimen_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(person_id_list), OMOP_PatientRecord.header_list).data_generate()
