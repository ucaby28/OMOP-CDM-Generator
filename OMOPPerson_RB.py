import OMOPPerson_RD as person
import Random as rd
import RuleBased_normal as rb

# messages to display at CLI
m1 = "Please enter the number of OMOP Person records you want to create: "
m2 = "Rule-based OMOP Person, Specimen, Measurement, Observation CSV tables generation complete!"


# the class that generate rule-based values for all the fields required in PERSON table
class OMOP_PatientRecord(rb.PatientRecord_RB):

    # generating a PERSON table and output as a csv file
    def data_generate(self):
        with open("Rule-based_OMOP_Person.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(self.records):
                writer.writerow({
                    "person_id": OMOP_PatientRecord.person_id,
                    "gender_concept_id": person.random.choice(person.gender_list),
                    "year_of_birth": self.dob_time().year,
                    "month_of_birth": self.dob_RB.month,
                    "day_of_birth": self.dob_RB.day,
                    "birth_datetime": self.dob_RB,
                    "race_concept_id": person.random.choice(person.race_list),
                    "ethnicity_concept_id": person.random.choice(person.ethnicity_list),
                    "location_id": person.random.choice(person.location_list)
                })
                OMOP_PatientRecord.person_id += 1
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(rd.main(m1, m2), person.OMOP_PatientRecord.header_list).data_generate()
    import OMOPSpecimen_RD as specimen
    import OMOPSpecimen_RB as specimen_rb
    specimen_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                   specimen.OMOP_PatientRecord.header_list).data_generate()
    import OMOPMeasurement_RD as measurement
    import OMOPMeasurement_RB as measurement_rb
    measurement_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      measurement.OMOP_PatientRecord.header_list).data_generate()
    import OMOPObservation_RD as observation
    import OMOPObservation_RB as observation_rb
    observation_rb.OMOP_PatientRecord(len(specimen_rb.person_id_list),
                                      observation.OMOP_PatientRecord.header_list).data_generate()
