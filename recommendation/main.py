
from recommendation.services import WeatherService, NetflixRouletteService, EventbriteService
from recommendation.recommender import Recommender

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/recommendations/', methods=['POST'])
def choice():

    recommender = Recommender(WeatherService(),
                              EventbriteService(),
                              NetflixRouletteService())

    return render_template("recommendations/choice.html",
                           recommendation=recommender.get_recommendation(request.form['latitude'], request.form['longitude']))


if __name__ == "__main__":
    app.run()
