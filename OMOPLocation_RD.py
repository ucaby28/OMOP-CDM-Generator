import OMOPPerson_RD as person
import Random as rd
import pandas as pd

# read CSV files for pre-stored IDs and store them into a list
location_id_file = 'config_files/measurement_concept_id.csv'
location_id_df = pd.read_csv(location_id_file)
location_id_list = location_id_df['Id']

# messages to display at CLI
m1 = "Please enter the number of OMOP Location records you want to create: "
m2 = "Random OMOP Location CSV generation complete!"


# the class that generate random values for all the fields required in Location table
class OMOP_PatientRecord(person.OMOP_PatientRecord):

    # define the column names for each field according to the OMOP CDM
    header_list = ["location_id", "city"]

    # generating a Location table and output as a csv file
    def data_generate(self):
        with open("Random_OMOP_Location.csv", 'wt') as OMOPcsvFile:
            writer = rd.csv.DictWriter(OMOPcsvFile, fieldnames=self.headers)
            writer.writeheader()
            for i in range(len(location_id_list)):
                writer.writerow({
                    "location_id": location_id_list[i],
                    "city": rd.fake.city(),
                })
            OMOPcsvFile.close()


if __name__ == "__main__":
    OMOP_PatientRecord(len(location_id_list), OMOP_PatientRecord.header_list).data_generate()
