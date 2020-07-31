import Random as rd
import numpy as np
import csv

# messages to display at CLI
m1 = "Please enter the number of patient records you want to create: "
m2 = "Rule-based Patient CSV generation complete!"


# generating selected fields with rule-based values
class PatientRecord_RB(rd.PatientRecord):

    # generating a rule-based date of birth from normal distribution and time with the corresponding age
    def dob_time(self):
        a = np.random.normal(40, 20)
        if a >= 0:
            self.age_dist = int(a)
            self.dob_year = self.this_year - self.age_dist
            self.dob_str = rd.fake1.date_time().isoformat()[4:]
            self.dob_RB = rd.dt.datetime.fromisoformat(str(self.dob_year) + self.dob_str)
        return self.dob_RB

    # output the rule-based values as a csv file
    def data_generate(self):
        with open("Rule-based_Patient_Data.csv", 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "PERSON_ID": PatientRecord_RB.person_id,
                    "Patient Name": rd.person_name(),
                    "BIRTH_DATETIME": self.dob_time(),
                    "Age": self.age_dist,
                    "Phone Number": rd.phone_num(),
                    "Address": self.address(),
                    "City": self.city,
                    "Postcode": self.postcode
                })
                PatientRecord_RB.person_id += 1
            csvFile.close()


if __name__ == "__main__":
    PatientRecord_RB(rd.main(m1, m2), PatientRecord_RB.header_list).data_generate()