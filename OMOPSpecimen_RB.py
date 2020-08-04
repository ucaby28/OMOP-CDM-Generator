import RuleBased_normal as rb
import OMOPRandomSpecimen as specimen
import Random as rd
import pandas as pd
import random

# read CSV files for pre-stored birth dates and store them into a list
person_file = 'Rule-based_OMOP_Person.csv'
person_df = pd.read_csv(person_file)
person_id_list = person_df['person_id']
person_year_of_birth_list = person_df['year_of_birth']

# messages to display at CLI
m1 = "Please enter the number of OMOP Specimen records you want to create: "
m2 = "Rule-based OMOP Specimen CSV generation complete!"


# the class that generate rule_based values for all the fields required in Specimen table
class OMOP_PatientRecord(rb.PatientRecord_RB):
    specimen_id = 1

    # define the column names for each field according to the OMOP CDM
    header_list = ["person_id", "specimen_id", "specimen_concept_id", "specimen_type_concept_id", "specimen_date"]

    def id(self):
        self.person_id = random.choice(person_id_list)
        self.person_age = int(rd.PatientRecord.this_year - person_year_of_birth_list[self.person_id - 1])
        return self.person_id

    # generating a Specimen table and output as a csv file
    def data_generate(self):
        with open("Rule-based_OMOP_Specimen.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": self.id(),
                    "specimen_id": OMOP_PatientRecord.specimen_id,
                    "specimen_concept_id": random.choice(specimen.specimen_concept_list),
                    "specimen_type_concept_id": random.choice(specimen.specimen_type_concept_list),
                    "specimen_date": rd.fake1.past_datetime(-365*self.person_age),
                })
                OMOP_PatientRecord.specimen_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(person_id_list), OMOP_PatientRecord.header_list).data_generate()
