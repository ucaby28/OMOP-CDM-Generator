import os

import OMOPPerson_RD as person
import Random as rd
import RuleBased_normal as rb

# messages to display at CLI
path = os.getcwd() + r'\OMOP_rule-based'
m2 = "Rule-based OMOP Person, Specimen, Measurement, Observation, and Location CSV tables generation complete!"


# the class that generate rule-based values for all the fields required in PERSON table
class OMOP_PatientRecord(rb.PatientRecord_RB):

    # generating a PERSON table and output as a csv file
    def data_generate(self, b, c, d, file_name):
        with open(file_name + "_Person.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": OMOP_PatientRecord.person_id,
                    "gender_concept_id": person.random.choice(person.gender_list),
                    "year_of_birth": self.dob_time(b, c, d).year,
                    "month_of_birth": self.dob_RB.month,
                    "day_of_birth": self.dob_RB.day,
                    "birth_datetime": self.dob_RB,
                    "race_concept_id": person.random.choice(person.race_list),
                    "ethnicity_concept_id": person.random.choice(person.ethnicity_list),
                    "location_id": person.random.choice(person.location_list)
                })
                OMOP_PatientRecord.person_id += 1
            OMOPcsvFile.close()
        print(m2)


if __name__ == "__main__":
    OMOP_PatientRecord(100, person.OMOP_PatientRecord.header_list).data_generate(40, 20, 'normal', path)
    import OMOPSpecimen_RD as specimen
    import OMOPSpecimen_RB as specimen_rb

    specimen_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                   specimen.OMOP_PatientRecord.header_list).data_generate(path)
    import OMOPMeasurement_RD as measurement
    import OMOPMeasurement_RB as measurement_rb

    measurement_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      measurement.OMOP_PatientRecord.header_list).data_generate(path)
    import OMOPObservation_RD as observation
    import OMOPObservation_RB as observation_rb

    observation_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      observation.OMOP_PatientRecord.header_list).data_generate(path)
    import OMOPLocation_RD as location
    import OMOPLocation_RB as location_rb

    location_rb.OMOP_PatientRecord(len(location.location_id_list),
                                   location.OMOP_PatientRecord.header_list).data_generate(path)
