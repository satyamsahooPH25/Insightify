import sys
sys.path.append(r"C:\Users\satya\Desktop\Insightify\Code_base\Scripts")
print(sys.path)
from CSV_Scripts.CSV_handler import CSV_Col_extractor
import os

def get_folder_path(prompt):
    while True:
        folder_path = input(prompt)
        if folder_path.startswith('"') and folder_path.endswith('"'):
            folder_path = folder_path[1:-1]  # Remove surrounding double quotes
        if os.path.exists(folder_path):
            return rf"{folder_path}"  
        else:
            print("Invalid path. Please enter a valid folder path.")

input_folder = get_folder_path("Enter the input folder path: ")
output_folder = get_folder_path("Enter the output folder path: ")
print("Input folder path:", input_folder)
print("Output folder path:", output_folder)
extractor = CSV_Col_extractor(input_folder, output_folder)

