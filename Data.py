import json
import os

File_Name = "Game_Production_Calendar_Data.json"

def Data_Founder(New_Data):
    try:
        if os.path.exists(File_Name):
            with open(File_Name, "r") as f:
                Data = json.load(f)
        else:
            Data = []
        Data.append(New_Data)
        with open(File_Name, "w") as f:
            json.dump(Data, f, indent=4)
    except Exception as e:
        print(f"An Error Has Occurued: {e}")

Test_Data = {
    "Project_Name": "First_Try",
    "İncome": 100,
    "Date": "22.04.2026"
}

Data_Founder(Test_Data)