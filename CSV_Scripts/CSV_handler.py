import os
import csv

class CSV_Col_extractor:
    def __init__(self,input_folder,output_folder):
        self.input_folder=input_folder
        self.output_folder=output_folder
        self.main()

    def extract_column_names(self,csv_file):
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            column_names = next(reader)
        return column_names
    def create_text_file(self,column_names, output_file):
        with open(output_file, 'w') as file:
            file.write('\n'.join(column_names))
    def main(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        for file_name in os.listdir(self.input_folder):
            try:
                if file_name.endswith('.csv'):
                    csv_file = os.path.join(self.input_folder, file_name)
                    column_names = self.extract_column_names(csv_file)
                    output_file = os.path.join(self.output_folder, file_name.replace('.csv', '_columns.txt'))
                    print(output_file)
                    self.create_text_file(column_names,output_file)
            except:
                continue
