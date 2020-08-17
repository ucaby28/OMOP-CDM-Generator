import OMOPLocation_RD as location
import Random as rd

# read CSV files for pre-stored UK cities names and store them into a list
UK_cities_file = 'config_files/UK_cities.csv'
UK_cities_df = location.pd.read_csv(UK_cities_file)
UK_cities_list = [uk for uk in UK_cities_df['city']]

# messages to display at CLI
m1 = "Please enter the number of OMOP Location records you want to create: "
m2 = "Rule-based OMOP Location CSV generation complete!"


# the class that generate rule_based values for all the fields required in Location table
class OMOP_PatientRecord(location.OMOP_PatientRecord):

    # generating the rule-based city location whenever possible. Use random city name if necessary.
    def find_city(self, num):
        self.city = rd.fake.city()
        while True:
            for i in UK_cities_list:
                if i.upper() in location.location_city_list[num].upper():
                    self.city = location.location_city_list[num]
            return location.location_id_list[num]

    # generating a Location table and output as a csv file
    def data_generate(self):
        with open("Rule-based_OMOP_Location.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(len(location.location_id_list)):
                writer.writerow({
                    "location_id": self.find_city(i),
                    "city": self.city,
                })
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(location.location_id_list), OMOP_PatientRecord.header_list).data_generate()
