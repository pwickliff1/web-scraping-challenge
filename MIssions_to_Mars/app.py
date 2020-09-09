# Dependencies
from flask import Flask, render_template, redirect
import scrape_mars_mission

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an  instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.facts.drop()


# create route that renders index.html template
@app.route("/")
def index():
    mars = db.facts.find_one()
    return render_template("index.html", mars=mars)


# Scrape the data
@app.route("/scrape")
def scraper():
    mars = db.facts
    mars_df = scrape_mars_mission.scrape()
    # mars_df.reset_index(drop=True)
    mars.update({}, mars_df, upsert=True)
 
    return redirect("/", code=302)
   


if __name__ == "__main__":
    app.run(debug=True)
