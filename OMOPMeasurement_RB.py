import OMOPSpecimen_RB as specimen_rb
import OMOPMeasurement_RD as measurement
import Random as rd
import random


# messages to display at CLI
m1 = "Please enter the number of OMOP Measurement records you want to create: "
m2 = "Rule-based OMOP Measurement CSV generation complete!"


# the class that generate rule_based values for all the fields required in Measurement table
class OMOP_PatientRecord(specimen_rb.OMOP_PatientRecord):
    measurement_id = 1

    # generating a Measurement table and output as a csv file
    def data_generate(self):
        with open("Rule-based_OMOP_Measurement.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "measurement_id": OMOP_PatientRecord.measurement_id,
                    "person_id": self.id()[0],
                    "measurement_concept_id": random.choice(measurement.measurement_concept_list),
                    "measurement_date": rd.fake1.past_datetime(-365 * self.person_age),
                    "measurement_type_concept_id": random.choice(measurement.measurement_type_concept_list),
                })
                OMOP_PatientRecord.measurement_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(specimen_rb.person_id_list), measurement.OMOP_PatientRecord.header_list).data_generate()
