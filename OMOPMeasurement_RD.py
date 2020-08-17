import OMOPPerson_RD as person
import OMOPSpecimen_RD as specimen
import Random as rd
import pandas as pd
import random

# read CSV files for pre-stored IDs and store them into a list
measurement_concept_file = 'config_files/measurement_concept_id.csv'
measurement_concept_df = pd.read_csv(measurement_concept_file)
measurement_concept_list = measurement_concept_df['Id']
measurement_type_concept_file = 'config_files/measurement_type_concept_id.csv'
measurement_type_concept_df = pd.read_csv(measurement_type_concept_file)
measurement_type_concept_list = measurement_type_concept_df['Id']

# messages to display at CLI
m1 = "Please enter the number of OMOP measurement records you want to create: "
m2 = "Random OMOP measurement CSV generation complete!"


# the class that generate random values for all the fields required in Measurement table
class OMOP_PatientRecord(person.OMOP_PatientRecord):
    measurement_id = 1

    # define the column names for each field according to the OMOP CDM
    header_list = ["measurement_id", "person_id", "measurement_concept_id", "measurement_date",
                   "measurement_type_concept_id"]

    # generating a Measurement table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Measurement.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "measurement_id": OMOP_PatientRecord.measurement_id,
                    "person_id": random.choice(specimen.person_id_list),
                    "measurement_concept_id": random.choice(measurement_concept_list),
                    "measurement_date": rd.fake1.date_time_ad().date(),
                    "measurement_type_concept_id": random.choice(measurement_type_concept_list),
                })
                OMOP_PatientRecord.measurement_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(specimen.person_id_list), OMOP_PatientRecord.header_list).data_generate()
