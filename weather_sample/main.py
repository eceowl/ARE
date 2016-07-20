from weather_sample.services import WeatherService, NetflixRouletteService, EventbriteService
from weather_sample.recommender import Recommender


class Application:
    def run(self):
        LATITUDE = 39.5
        LONGITUDE = -75.2

        recommender = Recommender(WeatherService(),
                                  EventbriteService(),
                                  NetflixRouletteService())

        recommender.get_recommendation(LATITUDE, LONGITUDE)


if __name__ == "__main__":
    app = Application()

    app.run()
