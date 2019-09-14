# coding=utf-8

import db
import htmlParser
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

db.openConnection()
db.loadVaccinesPriceListCsvToDb()

vaccinesByCountry = htmlParser.parseVaccinationsToTravelAbroadHtmlPage()

db.createVaccinesByCountryTable(vaccinesByCountry)

countries_options = db.getAllCountries()

@app.route('/')
def main_page():
    return render_template('index.html', countries=countries_options)

@app.route('/result/', methods=['POST'])
def result():
    country = request.form.get('country', 0)
    group = request.form.get('group', 0)

    records = db.getVaccinesByCountryAndGroup(country, group)

    for record in records[0][0].replace('{', '').replace('"', '').replace('}', '').split(','):
        print db.getVaccinePrice(record)

    data = {'vaccines': records[0][0].split(',')}
    data = jsonify(data)
    return data

app.run(host='0.0.0.0')

db.closeConnection()
