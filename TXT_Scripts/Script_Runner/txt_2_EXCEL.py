import sys
import os
sys.path.append(r"C:\Users\satya\Desktop\Insightify\Code_base\Scripts")
print(sys.path)
from TXT_Scripts.TXT_2_Excel import Txt2Excel
def get_folder_path(prompt):
    while True:
        folder_path = input(prompt)
        if folder_path.startswith('"') and folder_path.endswith('"'):
            folder_path = folder_path[1:-1]  # Remove surrounding double quotes
        if os.path.exists(folder_path):
            return rf"{folder_path}"  
        else:
            print("Invalid path. Please enter a valid folder path.")
input_txt_file=get_folder_path("Enter txt destination")
output_excel_file = get_folder_path("Enter excel destination")
extractor = Txt2Excel(input_txt_file,output_excel_file)