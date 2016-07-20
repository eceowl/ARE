from weather_sample.services import WeatherService, NetflixRouletteService, EventbriteService
from weather_sample.recommender import Recommender

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/recommendations/<latitude>,<longitude>')
def run(latitude, longitude):
    recommender = Recommender(WeatherService(),
                              EventbriteService(),
                              NetflixRouletteService())

    return jsonify(recommender.get_recommendation(latitude, longitude).serialize())


if __name__ == "__main__":
    app.run()
