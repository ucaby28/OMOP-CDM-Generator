import OMOPPerson_RB as person_rb
import OMOPSpecimen_RB as specimen_rb
import OMOPObservation_RD as observation
import Random as rd
import random


# messages to display at CLI
m1 = "Please enter the number of OMOP Observation records you want to create: "
m2 = "Rule-based OMOP Observation CSV generation complete!"


# the class that generate rule_based values for all the fields required in Observation table
class OMOP_PatientRecord(specimen_rb.OMOP_PatientRecord):
    observation_id = 1

    # generating a Observation table and output as a csv file
    def data_generate(self, file_name):
        with open(file_name + "_Observation.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "observation_id": OMOP_PatientRecord.observation_id,
                    "person_id": self.id()[0],
                    "observation_concept_id": random.choice(observation.observation_concept_list),
                    "observation_date": rd.fake1.past_datetime(-365 * self.person_age),
                    "observation_type_concept_id": random.choice(observation.observation_type_concept_list),
                })
                OMOP_PatientRecord.observation_id += 1
            OMOPcsvFile.close()
        print(m2)


if __name__ == "__main__":
    OMOP_PatientRecord(len(specimen_rb.person_id_list),
                       observation.OMOP_PatientRecord.header_list).data_generate(person_rb.path)
