
from recommendation.services import WeatherService, NetflixRouletteService, EventbriteService
from recommendation.recommender import Recommender

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/recommendations/', methods=['POST'])
def choice():

    latitude = int(request.form['latitude'])
    longitude = int(request.form['longitude'])

    # This should return something prettier
    if latitude < -90 or latitude > 90:
        return "Invalid latitude range"
    if longitude < -180 or longitude > 180:
        return "Invalid longitude range"

    recommender = Recommender(WeatherService(),
                              EventbriteService(),
                              NetflixRouletteService())

    return render_template("recommendations/choice.html",
                           recommendation=recommender.get_recommendation(request.form['latitude'], request.form['longitude']))


if __name__ == "__main__":
    app.run()
