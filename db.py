import psycopg2

conn = None

def openConnection():
  global conn
  conn = psycopg2.connect(database="akvtcxli", user="akvtcxli", password="Rw8H6CodGsivtOpMRJeeQc2BVTv68z1L", host="manny.db.elephantsql.com", port="5432")

def closeConnection():
  conn.close()

def loadVaccinesPriceListCsvToDb():
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS vaccines_price_list;")
  cur.execute("CREATE TABLE vaccines_price_list (secondaryId TEXT, id TEXT PRIMARY KEY, description TEXT, disease TEXT, price TEXT, customerPrice TEXT, comment TEXT, map TEXT);")
  
  with open('vaccines-price-list.csv', 'r') as f:
    next(f) # Skip the header row
    cur.copy_from(f, 'vaccines_price_list', sep=',')
  
  conn.commit()

def createVaccinesByCountryTable(vaccinesByCountry):
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS vaccines_by_country;")
  cur.execute("CREATE TABLE vaccines_by_country (country TEXT PRIMARY KEY, group1 TEXT, group2 TEXT, group3 TEXT);")
  
  for vaccines in vaccinesByCountry:
    cur.execute("INSERT INTO vaccines_by_country (country, group1, group2, group3) VALUES (%s, %s, %s, %s)", (vaccines["country"], vaccines["group1"], vaccines["group2"], vaccines["group3"]))
  
  conn.commit()