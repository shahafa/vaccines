import db
import htmlParser

db.openConnection()
db.loadVaccinesPriceListCsvToDb()

vaccinesByCountry = htmlParser.parseVaccinationsToTravelAbroadHtmlPage()

db.createVaccinesByCountryTable(vaccinesByCountry)

selectedCountry = input("הקש מדינה: ")
selectedGroup = input("הקש מספר קבוצה: ")

for vaccines in vaccinesByCountry:
  if vaccines["country"] == selectedCountry:
    selectedGroupString = "group{0}".format(selectedGroup)
    index = 1
    for word in vaccines[selectedGroupString]:
      print(str(index)+": " + word)
      index +=1

db.closeConnection()
