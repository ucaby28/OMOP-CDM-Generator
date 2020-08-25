import RuleBased_normal as rb
import OMOPPerson_RB as person_rb
import OMOPSpecimen_RD as specimen
import Random as rd
import pandas as pd
import random

# read CSV files for pre-stored birth dates and store them into a list
# try:
person_file = person_rb.path + '_Person.csv'
person_df = pd.read_csv(person_file)
person_id_list = person_df['person_id']
person_year_of_birth_list = person_df['year_of_birth']
# except FileNotFoundError:
#     print('Please create a Person table before other OMOP rule-based tables')

# messages to display at CLI
m1 = "Please enter the number of OMOP Specimen records you want to create: "
m2 = "Rule-based OMOP Specimen CSV generation complete!"


# the class that generate rule_based values for all the fields required in Specimen table
class OMOP_PatientRecord(rb.PatientRecord_RB):
    specimen_id = 1

    def id(self):
        self.person_id = random.choice(person_id_list)
        self.person_age = int(rd.PatientRecord.this_year - person_year_of_birth_list[self.person_id - 1])
        return self.person_id, self.person_age

    # generating a Specimen table and output as a csv file
    def data_generate(self, file_name):
        with open(file_name + "_Specimen.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": self.id()[0],
                    "specimen_id": OMOP_PatientRecord.specimen_id,
                    "specimen_concept_id": random.choice(specimen.specimen_concept_list),
                    "specimen_type_concept_id": random.choice(specimen.specimen_type_concept_list),
                    "specimen_date": rd.fake1.past_datetime(-365*self.person_age),
                })
                OMOP_PatientRecord.specimen_id += 1
            OMOPcsvFile.close()
        print(m2)


if __name__ == "__main__":
    OMOP_PatientRecord(len(person_id_list), specimen.OMOP_PatientRecord.header_list).data_generate(person_rb.path)
