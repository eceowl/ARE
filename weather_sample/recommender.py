import random
import pprint
from weather_sample.resources import Recommendation


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    @staticmethod
    def __is_stay_in_weather__(weather_by_hour):
        return weather_by_hour['apparentTemperature'] < 30 or \
               weather_by_hour['apparentTemperature'] > 95 or \
               weather_by_hour['precipProbability'] > .7

    def __get_netflix_recommendation__(self):
        shows = self.netflix_service.get_netflix_shows()

        # TODO actually create a recommendation algorithm
        show = random.choice(shows)

        info = self.netflix_service.get_show_information(show)
        return Recommendation(info['title'], info['overview'], info['url'], "Netflix")

    def __get_eventbrite_recommendation__(self, latitude, longitude):
        events = self.eventbrite_service.get_events_around(latitude, longitude)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(events)
        if len(events) == 0:
            return self.__get_netflix_recommendation__()

        event = random.choice(events)

        recommendation = Recommendation(
            event['name']['text'],
            event['description']['text'],
            event['url'],
            "Eventbrite"
        )

        return recommendation

    def get_recommendation(self, latitude, longitude):
        hourly_weather = self.weather_service.get_hourly_weather(latitude, longitude)

        if any(self.__is_stay_in_weather__(hour) for hour in hourly_weather['data']):
            return self.__get_netflix_recommendation__()
        else:
            return self.__get_eventbrite_recommendation__(latitude, longitude)
