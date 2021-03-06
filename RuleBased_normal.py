import os

import Random as rd
import numpy as np
import csv

# messages to display at CLI
m2 = "Rule-based Patient CSV generation complete!"


# generating selected fields with rule-based values
class PatientRecord_RB(rd.PatientRecord):

    # generating a rule-based date of birth from normal distribution and time with the corresponding age
    def dob_time(self, b, c, d):
        while True:
            try:
                if self.check_dist(b, c, d) >= 0:
                    self.age_dist = int(self.res)
                    self.dob_year = self.this_year - self.age_dist
                    self.dob_str = rd.fake1.date_time().isoformat()[4:]
                    self.dob_RB = rd.dt.datetime.fromisoformat(str(self.dob_year) + self.dob_str)
                return self.dob_RB
            except Exception:
                continue

    def check_dist(self, b, c, d):
        if d.strip() == 'normal':
            self.res = float(np.random.normal(b, c))
        elif d.strip() == 'binomial':
            self.res = float(np.random.binomial(c, b))
        elif d.strip() == 'poisson':
            self.res = float(np.random.poisson(b))
        return self.res

    # output the rule-based values as a csv file
    def data_generate(self, b, c, d, file_name):
        with open(file_name + '.csv', 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=self.headers)
            writer.writeheader()

            for i in range(self.records):
                writer.writerow({
                    "PERSON_ID": PatientRecord_RB.person_id,
                    "Patient Name": rd.person_name(),
                    "BIRTH_DATETIME": self.dob_time(b, c, d),
                    "Age": self.age_dist,
                    "Phone Number": rd.phone_num(),
                    "Address": self.address(),
                    "City": self.city,
                    "Postcode": self.postcode
                })
                PatientRecord_RB.person_id += 1
            csvFile.close()
        print(m2)


if __name__ == "__main__":
    PatientRecord_RB(100, PatientRecord_RB.header_list).data_generate(40, 20, 'normal',
                                                                      os.getcwd() + r'\Rule-based')
