from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'

if __name__ == "__main__":
    app.run(debug=True)