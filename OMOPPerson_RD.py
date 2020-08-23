import random
import pandas as pd
import Random as rd

# read CSV files for pre-stored IDs and store them into a list
gender_file = 'config_files/gender_id.csv'
gender_df = pd.read_csv(gender_file)
gender_list = gender_df['Id']
race_file = 'config_files/race_id.csv'
race_df = pd.read_csv(race_file)
race_list = race_df['Id']
ethnicity_file = 'config_files/ethnicity_id.csv'
ethnicity_df = pd.read_csv(ethnicity_file)
ethnicity_list = ethnicity_df['Id']
location_file = 'config_files/location_id.csv'
location_df = pd.read_csv(location_file)
location_list = location_df['Id']

# messages to display at CLI
m2 = "Random OMOP Person, Specimen, Measurement, Observation, and Location CSV tables generation complete!"


# the class that generate random values for all the fields required in PERSON table
class OMOP_PatientRecord(rd.PatientRecord):
    # define the column names for each field according to the OMOP CDM
    header_list = ["person_id", "gender_concept_id", "year_of_birth", "month_of_birth", "day_of_birth",
                   "birth_datetime", "race_concept_id", "ethnicity_concept_id", "location_id"]

    # generating a PERSON table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Person.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": OMOP_PatientRecord.person_id,
                    "gender_concept_id": random.choice(gender_list),
                    "year_of_birth": self.dob_time().year,
                    "month_of_birth": self.sdg_dob.month,
                    "day_of_birth": self.sdg_dob.day,
                    "birth_datetime": self.sdg_dob,
                    "race_concept_id": random.choice(race_list),
                    "ethnicity_concept_id": random.choice(ethnicity_list),
                    "location_id": random.choice(location_list)
                })
                OMOP_PatientRecord.person_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(rd.main(100, m2), OMOP_PatientRecord.header_list).data_generate()
    import OMOPSpecimen_RD as specimen

    specimen.OMOP_PatientRecord(len(specimen.person_id_list),
                                specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement

    measurement.OMOP_PatientRecord(len(specimen.person_id_list),
                                   measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation

    observation.OMOP_PatientRecord(len(specimen.person_id_list),
                                   observation.OMOP_PatientRecord.header_list).data_generate()
    import OMOPLocation_RD as location

    location.OMOP_PatientRecord(len(location.location_id_list),
                                location.OMOP_PatientRecord.header_list).data_generate()

