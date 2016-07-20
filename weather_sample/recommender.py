import random
import pprint


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    @staticmethod
    def __is_stay_in_weather__(weather_by_hour):
        return weather_by_hour['apparentTemperature'] < 30 or \
               weather_by_hour['apparentTemperature'] > 100 or \
               weather_by_hour['precipProbability'] > .7

    def get_recommendation(self, latitude, longitude):
        hourly_weather = self.weather_service.get_hourly_weather(latitude, longitude)
        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(hourly_weather)
        if any(self.__is_stay_in_weather__(hour) for hour in hourly_weather['data']):
            shows = self.netflix_service.get_netflix_shows()
            pp.pprint(shows)

            # TODO actually create a recommendation algorithm
            show = random.choice(shows)

            return self.netflix_service.get_show_information(show)

        else:
            return self.eventbrite_service.get_events_around(latitude, longitude)
