from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
print("this is a test")
@app.route('/')
def index():
    print("this is a test")
    return render_template('test.html')


# @app.route("/")
# def home():

#     # Find one record of data from the mongo database
#     destination_data = mongo.db.collection.find_one()

#     # Return template and data
#     return render_template("inddddddex.html", Mars=destination_data)

# @app.route('/')
# def index():
#     return "This is a test"
    # print("print tests")
    # mars_data = mongo.db.marsData.find_one()
    # print(mars_data)
    # return render_template("index.html", mars=mars_data)

@app.route('/scrape')
def scrape():

    marsDB = mongo.db.marsData

    mongo.db.marsData.drop()
    
    mars_data = scrape_mars.scrape()

    marsDB.insert_one(mars_data)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)