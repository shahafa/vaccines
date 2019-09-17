# coding=utf-8

import db
import htmlParser
from flask import Flask, render_template, request, jsonify
import re

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

    res = []
    for record in re.sub('({|}|"|-)', '', records[0][0]).split(','):
        res.append({
            "name": record,
            "price": sum(map(lambda x: int(x[0]) if x[0] is not None else 0, db.getVaccinePrice(record)))
        })

    return (jsonify(res))

app.run(host='0.0.0.0')
