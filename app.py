from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"

mongo = PyMongo(app)

@app.route("/")
def home():

  # Find one record of data from the mongo database
  mars_data = mongo.db.marsData.find_one()

  # Return template and data
  return render_template("index.html", mars=mars_data)


@app.route('/scrape')
def scrape():

    marsTable = mongo.db.marsData

    # Drop old data so we can re run app
    mongo.db.marsData.drop()

    # Run the scrape function
    mars_data = scrape_mars.Scrape_All()

    # Insert new record of data
    marsTable.insert_one(mars_data)

    return redirect("/")

if __name__ == '__main__':
    app.run()