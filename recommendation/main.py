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
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except ValueError:
        return render_template("error.html", message="Invalid latitude and/or longitude values, must be numbers.")

    # This should return something prettier
    if latitude < -90 or latitude > 90:
        return render_template("error.html", message="Invalid latitude range must be between -90 and 90")
    if longitude < -180 or longitude > 180:
        return render_template("error.html", message="Invalid longitude range must be between -180 and 180")

    return render_template("recommendations/choice.html",
                           recommendation=recommender.get_recommendation(latitude, longitude))


if __name__ == "__main__":
    app.run()
