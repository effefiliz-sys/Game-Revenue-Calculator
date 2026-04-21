import pandas 

def save_to_excel(data_packet):
    try:
        df = pandas.DataFrame([data_packet])

        df.to_excel("Game_Revenue_Data.xlsx", index=False)
        print("\n[SUCCES] Data has been exported to Excel succesfully")
    except Exception as e:
        print(f"\n[ERROR] an error occurred while writing to Excel: {e}")