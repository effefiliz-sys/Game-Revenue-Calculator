from Excel import save_to_excel

Hun = 0.27 #Hungary
Den = 0.25 #Denmark
Tur = 0.20 #Turkey
Uni = 0.20 #United Kingdom
Ger = 0.19 #Germany
Prc = 0.13 #China
Ind = 0.18 #India
Kor = 0.10 #South Korea
Jap = 0.10 #Japan
Usa = 0.07 #United States of America

#Store Commision
steam = 0.30
Epic_Games = 0.12
gog = 0.30
Play_Store = 0.15
App_Store = 0.30
Xbox = 0.30
PlayStation = 0.30


gross_revenue = float(input(" Please Enter Gross Revenue "))

Which_Country = input(" Please Enter Your Country ")

if Which_Country == "Hungary":
    selected_tax = Hun
elif Which_Country == "Denmark":
    selected_tax = Den
elif Which_Country == "Turkey":
    selected_tax = Tur
elif Which_Country == "United Kingdom":
    selected_tax = Uni
elif Which_Country == "Germany":
    selected_tax = Ger
elif Which_Country == "China":
    selected_tax = Prc
elif Which_Country == "India":
    selected_tax = Ind
elif Which_Country == "Korea":
    selected_tax = Kor
elif Which_Country == "Japan":
    selected_tax = Jap
elif Which_Country == "America" or Which_Country == "USA":
    selected_tax = Usa
else:
    print(" Please Try Again: This country is not supported yet. ")
    selected_tax = 0

process1 = gross_revenue * (1 - selected_tax) 
print(process1)

Which_Platform = input("Enter The Platform Where İt Was Published  ")

if Which_Platform == "Steam":
    selected_Platform = steam
elif Which_Platform == "Epic Games":
    selected_Platform = Epic_Games
elif Which_Platform == "GOG":
    selected_Platform = gog
elif Which_Platform == "Play Store":
    selected_Platform = Play_Store
elif Which_Platform == "App Store":
    selected_Platform = App_Store
elif Which_Platform == "Xbox":
    selected_Platform = Xbox
elif Which_Platform == "Playstation":
    selected_Platform = PlayStation
else:
    print(" This Platform İs Not Supported ")
    selected_Platform = 0

process2 = process1 * (1 - selected_Platform)
print(process2)

Publisher_Answer = input(" Did this project receive publisher support ").lower()

if Publisher_Answer == "yes":
    has_publisher = True
else:
    has_publisher = False

if has_publisher == True:
   Publisher_Share = int(input(" Enter the Publisher's Share ")) / 100
else:
    Publisher_Share = 0
    
process3 = process2 * (100 - Publisher_Share) / 100
print(process3)

Development_Spent = int(input("Enter the budget spent on the development process "))

Process4 = process3 - Development_Spent
print(Process4)

User_Want_ExcelData = input("Do you want write this data to excel file ").lower()

if User_Want_ExcelData.startswith("y"):
    export_data = {
    "Country": Which_Country,
    "Platform": Which_Platform,
    "Gross_Revenue": gross_revenue,
    "Net_Profit": Process4,
    "Tax_Amount": selected_tax,
    "Store_Cut": process2
    }

    save_to_excel(export_data)
else:
    print("Excel writing has been refused ")

print("Thankyou for using my program <3 ")