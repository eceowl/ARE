from recommendation.services import WeatherService, NetflixRouletteService, EventbriteService
from recommendation.recommender import Recommender

from flask import Flask, render_template, request

app = Flask(__name__)

recommender = Recommender(
    WeatherService(),
    EventbriteService(),
    NetflixRouletteService()
)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/recommendations/', methods=['GET'])
def choice():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))

    # This should return something prettier
    if latitude < -90 or latitude > 90:
        return "Invalid latitude range"
    if longitude < -180 or longitude > 180:
        return "Invalid longitude range"

    return render_template("recommendations/choice.html",
                           recommendation=recommender.get_recommendation(latitude, longitude))


if __name__ == "__main__":
    app.run()
