import random
from recommendation.resources import Recommendation


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    @staticmethod
    def __is_stay_in_weather__(weather_by_hour):
        # Arbitrary number choices for now
        # TODO make this a little more advanced
        return weather_by_hour['temperature'] < 30 or \
               weather_by_hour['temperature'] > 95 or \
               weather_by_hour['precipProbability'] > .7

    def __get_netflix_recommendation__(self):
        shows = self.netflix_service.get_netflix_shows()

        # TODO actually create a recommendations algorithm for shows
        show = random.choice(shows)

        info = self.netflix_service.get_show_information(show)

        recommendation = Recommendation(
            info['title'],
            info['overview'],
            info['url'],
            "Netflix"
        )

        return recommendation

    def __get_eventbrite_recommendation__(self, latitude, longitude):
        events = self.eventbrite_service.get_events_around(latitude, longitude)

        if len(events) == 0:
            return self.__get_netflix_recommendation__()

        # TODO actually create a recommendations algorithm for events
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

        # TODO add more fine grained detail as to why recommendations was given
        # i.e. 'It's too hot outside!' or 'It's raining!'

        if any(self.__is_stay_in_weather__(hour) for hour in hourly_weather['data']):
            return self.__get_netflix_recommendation__()
        else:
            return self.__get_eventbrite_recommendation__(latitude, longitude)
