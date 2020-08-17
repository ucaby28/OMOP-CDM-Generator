import OMOPPerson_RD as person
import OMOPSpecimen_RD as specimen
import Random as rd
import pandas as pd
import random

# read CSV files for pre-stored IDs and store them into a list
observation_concept_file = 'config_files/observation_concept_id.csv'
observation_concept_df = pd.read_csv(observation_concept_file)
observation_concept_list = observation_concept_df['Id']
observation_type_concept_file = 'config_files/observation_type_concept_id.csv'
observation_type_concept_df = pd.read_csv(observation_type_concept_file)
observation_type_concept_list = observation_type_concept_df['Id']

# messages to display at CLI
m1 = "Please enter the number of OMOP observation records you want to create: "
m2 = "Random OMOP observation CSV generation complete!"


# the class that generate random values for all the fields required in Measurement table
class OMOP_PatientRecord(person.OMOP_PatientRecord):
    observation_id = 1

    # define the column names for each field according to the OMOP CDM
    header_list = ["observation_id", "person_id", "observation_concept_id", "observation_date",
                   "observation_type_concept_id"]

    # generating a Observation table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Observation.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "observation_id": OMOP_PatientRecord.observation_id,
                    "person_id": random.choice(specimen.person_id_list),
                    "observation_concept_id": random.choice(observation_concept_list),
                    "observation_date": rd.fake1.date_time_ad().date(),
                    "observation_type_concept_id": random.choice(observation_type_concept_list),
                })
                OMOP_PatientRecord.observation_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(specimen.person_id_list), OMOP_PatientRecord.header_list).data_generate()
